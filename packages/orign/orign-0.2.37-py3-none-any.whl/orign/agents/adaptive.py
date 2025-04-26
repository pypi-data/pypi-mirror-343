from typing import Any, Dict, List, Optional

from chatmux import ChatRequest, ChatResponse
from namesgenerator import get_random_name
from nebu import Message, Processor, processor

from orign.actors.models import Action
from orign.humans.human import Human
from orign.humans.models import V1Feedback as Feedback
from orign.llms.llm import OnlineLLM
from orign.mcp import MCPClient
from orign.zoo.llms.qwen_vl import QwenVL2_5


class AdaptiveAgent:
    """An agent that can learn to adapt to its environment."""

    def __init__(
        self,
        mcp_config: Dict[str, Any],
        server_name: str,
        observation: Action,
        max_steps: int = 30,
        name: Optional[str] = None,
        llm: Optional[OnlineLLM[ChatRequest, ChatResponse, ChatRequest]] = None,
        platform: str = "runpod",
        model: str = "unsloth/Qwen2.5-VL-32B-Instruct",
        accelerators: List[str] = ["1:A100_SXM"],
        human_medium: str = "ui",
        interactive: bool = True,
        initial_action: Optional[Action] = None,
        namespace: Optional[str] = None,
    ):
        if not name:
            name = get_random_name("-")
            if not name:
                raise ValueError("Name cannot be None")
        if not llm:
            llm = QwenVL2_5(
                name=name, platform=platform, model=model, accelerators=accelerators
            )

        self.llm = llm
        self.max_steps = max_steps
        self.client = MCPClient(mcp_config)
        self.session = self.client.new_session(server_name)
        self.interactive = interactive
        self.human_medium = human_medium
        self.namespace = namespace
        feedback_proc = new_feedback_processor(
            llm=llm, platform=platform, namespace=namespace
        )
        self.human = Human(
            name=name,
            namespace=namespace,
            medium=self.human_medium,
            callback=feedback_proc,
        )
        self.result = None
        self.initial_action = initial_action
        self.observation = observation

    def ctx(self, task: str):
        return f"""You are operating a web browser helping accomplish tasks.
Please help complete the task '{task}' with the tools: {self.session.discover_tools()}
Given the current screenshot of the browser, please select your next action.
Please output the action in a JSON format, following the example:
{{
    "action": "browser_navigate",
    "parameters": {{
        "url": "https://flights.google.com"
    }}
}}
If you are done, simple return the `end` action.
"""

    def solve(
        self,
        task: str,
        max_steps: int = 30,
    ):
        if self.initial_action:
            self.session.call_tool(
                self.initial_action.name, self.initial_action.parameters
            )

        max_steps = max_steps or self.max_steps
        for i in range(max_steps):
            print(">>> taking step: ", i)

            # Take screenshot
            output = self.session.call_tool(
                self.observation.name, self.observation.parameters
            )
            image_b64 = output.content[0].data
            mime_type = getattr(output.content[0], "mimeType", "image/jpeg")

            # Construct data URI for OpenAI
            data_uri = f"data:{mime_type};base64,{image_b64}"

            # Build messages for vision model
            messages = {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.ctx(task)},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": data_uri,
                                },
                            },
                        ],
                    }
                ]
            }

            # Generate an action
            resp = self.llm.generate(messages)
            content = resp.choices[0].message.content
            print("llm generated content: ", content)
            if not content:
                print("No content, skipping")
                continue

            try:
                action = Action.model_validate_json(content)
            except Exception as e:
                print(f"Error validating action: {e}")
                continue

            if action.name == "end":
                print("Done!")
                break

            # Take mcp action
            print(f"Taking action: {action.name} with parameters: {action.parameters}")
            try:
                self.session.call_tool(action.name, action.parameters)
            except Exception as e:
                print(f"Error taking action: {e}")
                continue
            print("Action taken")

            # append response
            messages["messages"].append({"role": "assistant", "content": content})

            # Ask a human for feedback, waiting to continue loop until approved
            self.human.feedback(
                "Was this action correct?", messages=messages, wait=self.interactive
            )

        # Now lets use all the feedback we collected to fine-tune the LLM!
        if self.interactive:
            print("Training the LLM")
            self.llm.train()


def new_feedback_processor(
    llm: OnlineLLM,
    image: str = "python:3.11-slim",
    platform: str = "runpod",
    namespace: Optional[str] = None,
) -> Processor:
    @processor(image=image, platform=platform, namespace=namespace)
    def on_feedback(message: Message[Feedback]):
        # Parse the feedback from the message
        feedback = message.content
        if not feedback:
            print("No feedback, skipping")
            return

        response = feedback.response
        if not response:
            print("No response from the user, skipping")
            return

        if response.approved and feedback.request.messages:
            # Send to the LLM to learn
            print(f"Learning from feedback: {feedback.request.messages}")
            llm.learn(feedback.request.messages)

    return on_feedback
