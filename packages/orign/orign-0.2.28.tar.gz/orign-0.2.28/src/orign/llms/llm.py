import time
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

import requests
from chatmux import ChatRequest
from nebu import V1ResourceMetaRequest, V1ResourceReference
from pydantic import BaseModel, TypeAdapter

from orign.auth import get_user_profile
from orign.buffers.models import V1ReplayBufferData
from orign.config import GlobalConfig
from orign.llms.models import (
    V1OnlineLLM,
    V1OnlineLLMRequest,
    V1OnlineLLMs,
    V1OnlineLLMStatus,
    V1UpdateOnlineLLMRequest,
)
from orign.trainings.models import V1TrainingStatus
from orign.trainings.training import Training

InputType = TypeVar("InputType", bound=BaseModel)
OutputType = TypeVar("OutputType", bound=BaseModel)
ExampleType = TypeVar("ExampleType", bound=BaseModel)


class OnlineLLM(Generic[InputType, OutputType, ExampleType]):
    """
    Online LLMs can both learn and act.
    """

    def __init__(
        self,
        name: str,
        model: str,
        server: V1ResourceReference,
        buffer: V1ResourceReference,
        trainer: V1ResourceReference,
        train_args: Optional[Dict[str, Any]] = None,
        train_every: Optional[int] = None,
        train_n: Optional[int] = None,
        train_strategy: Optional[str] = None,
        namespace: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        adapter: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
        no_delete: bool = False,
    ):
        self.config = config or GlobalConfig.read()
        current_server = self.config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        self.api_key = current_server.api_key
        self.orign_host = current_server.server
        self.name = name
        self.namespace = namespace
        self.labels = labels
        self.model = model
        self.llms_url = f"{self.orign_host}/v1/llms"
        self.adapter = adapter

        # Fetch existing LLMs
        response = requests.get(
            self.llms_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()

        name_parts = name.split("/")
        if len(name_parts) == 2:
            self.namespace = name_parts[0]
            self.name = name_parts[1]
        else:
            self.namespace = None
            self.name = name

        if not namespace:
            if not self.api_key:
                raise ValueError("No API key provided")

            user_profile = get_user_profile(self.api_key)
            namespace = user_profile.handle

            if not namespace:
                namespace = user_profile.email.replace("@", "-").replace(".", "-")

        print(f"Using namespace: {namespace}")

        existing_llms = V1OnlineLLMs.model_validate(response.json())
        self.llm: Optional[V1OnlineLLM] = next(
            (
                llm_val
                for llm_val in existing_llms.llms
                if llm_val.metadata.name == name
                and llm_val.metadata.namespace == namespace
            ),
            None,
        )

        # If not found, create
        if not self.llm:
            request = V1OnlineLLMRequest(
                metadata=V1ResourceMetaRequest(
                    name=name,
                    namespace=namespace,
                    labels=labels,
                ),
                model=model,
                buffer=buffer,
                server=server,
                trainer=trainer,
                train_args=train_args,
            )
            print("Request:")
            print(request.model_dump_json())
            create_response = requests.post(
                self.llms_url,
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            create_response.raise_for_status()
            self.llm = V1OnlineLLM.model_validate(create_response.json())
            print(f"Created LLM {self.llm.metadata.name}")
        else:
            # Else, update
            print(f"Found LLM {self.llm.metadata.name}, updating if necessary")
            update_request = V1UpdateOnlineLLMRequest(
                buffer=buffer,
                server=server,
                no_delete=no_delete,
            )
            print("Update request:")
            print(update_request.model_dump_json())
            patch_response = requests.patch(
                f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}",
                json=update_request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            patch_response.raise_for_status()
            print(f"Updated LLM {self.llm.metadata.name}")

    def generate(self, data: InputType | Dict[str, Any]) -> OutputType:
        """
        Generate an output from the LLM.
        """
        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        validated_input: InputType
        if isinstance(data, dict):
            # Convert dict to the InputType model
            validated_input = TypeAdapter(InputType).validate_python(data)
        else:
            # It's already InputType, assign it directly
            validated_input = data

        if isinstance(validated_input, ChatRequest):
            validated_input.model = (
                f"{self.llm.metadata.namespace}/{self.llm.metadata.name}"
            )

        url = f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}/generate"

        request = {
            "model": self.model,
            # Use the validated input which is guaranteed to be InputType
            "input": validated_input.model_dump(),
        }

        response = requests.post(
            url,
            json=request,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        adapter = TypeAdapter(OutputType)

        return adapter.validate_python(response.json())

    def train(self, wait: bool = False) -> dict:
        """
        Train the LLM.
        """
        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        url = f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}/train"
        response = requests.post(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        # {
        #     "success": true,
        #     "stream_id": stream_id,
        #     "message_id": message.id
        # }
        message_id = response.json()["message_id"]
        print(f"Training message_id: {message_id}")
        if wait:
            while True:
                trainings = Training.get(
                    namespace=self.namespace,
                    adapter_name=self.name,
                    labels={"message_id": message_id},
                )
                if trainings:
                    training = trainings[0]
                    if training.status == V1TrainingStatus.COMPLETED:
                        print("Training completed!")
                        break
                    else:
                        print(f"Training status: {training.status}")
                else:
                    print("Wating for training to start...")
                time.sleep(5)
        return response.json()

    def learn(
        self,
        examples: Union[Dict[str, Any], List[Dict[str, Any]], ExampleType],
        train: bool = False,
    ):
        """
        Learn from a list of examples.

        Examples can be:
        - A single dictionary representing a conversation.
        - A list of dictionaries, each representing a conversation.
        - An instance of the ExampleType model.
        """

        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        processed_examples: List[Dict[str, Any]]

        if isinstance(examples, dict):
            processed_examples = [examples]
        elif isinstance(examples, list):
            # Assume list contains Dict[str, Any] as per the type hint
            processed_examples = examples
        elif isinstance(examples, BaseModel):  # type: ignore [misc] # Check against the bound type BaseModel
            # If it's a BaseModel (our ExampleType instance), dump it to dict
            processed_examples = [examples.model_dump()]
        else:
            # Raise an error for unexpected types
            raise TypeError(f"Unsupported type for examples: {type(examples).__name__}")

        url = f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}/learn"
        # Now processed_examples is guaranteed to be List[Dict[str, Any]]
        request = V1ReplayBufferData(examples=processed_examples, train=train)

        response = requests.post(
            url,
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

        response.raise_for_status()
        return response.json()

    @classmethod
    def load(
        cls,
        name: str,
        namespace: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ):
        """
        Get an LLM from the remote server.
        """
        llms = cls.get(namespace=namespace, name=name, config=config)
        if not llms:
            raise ValueError("LLM not found")
        llm_v1 = llms[0]

        out = cls.__new__(cls)
        out.llm = llm_v1
        out.config = config or GlobalConfig.read()
        current_server = out.config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        out.api_key = current_server.api_key
        out.orign_host = current_server.server
        out.llms_url = f"{out.orign_host}/v1/llms"
        out.name = name
        out.namespace = namespace
        out.model = llm_v1.model
        return out

    @classmethod
    def get(
        cls,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ) -> List[V1OnlineLLM]:
        """
        Get a list of LLMs that match the optional name and/or namespace filters.
        """
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        llms_url = f"{current_server.server}/v1/llms"

        response = requests.get(
            llms_url, headers={"Authorization": f"Bearer {current_server.api_key}"}
        )
        response.raise_for_status()

        llms_response = V1OnlineLLMs.model_validate(response.json())
        filtered_llms = llms_response.llms

        if name:
            filtered_llms = [llm for llm in filtered_llms if llm.metadata.name == name]
        if namespace:
            filtered_llms = [
                llm for llm in filtered_llms if llm.metadata.namespace == namespace
            ]

        return filtered_llms

    def delete(self):
        """
        Delete the LLM.
        """
        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        url = f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}"
        response = requests.delete(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return

    def status(self) -> V1OnlineLLMStatus:
        """
        Get the status of the LLM.
        """
        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        llms = self.get(
            namespace=self.llm.metadata.namespace, name=self.llm.metadata.name
        )
        if not llms:
            raise ValueError("LLM not found")
        llm = llms[0]

        return llm.status

    def ref(self) -> str:
        """
        Get the resource ref for the container.
        """
        return f"{self.name}.{self.namespace}.Container"
