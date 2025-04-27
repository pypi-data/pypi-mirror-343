import time
from typing import Any, Dict, List, Optional

import requests
from nebu import Processor
from nebu.meta import V1ResourceMetaRequest, V1ResourceReference

from orign.config import GlobalConfig
from orign.humans.models import (
    V1ApprovalRequest,
    V1ApprovalResponse,
    V1FeedbackItem,
    V1FeedbackRequest,
    V1FeedbackResponse,
    V1Human,
    V1HumanMessage,
    V1HumanRequest,
    V1Humans,
    V1UpdateHumanRequest,
)


class Human:
    def __init__(
        self,
        name: str,
        medium: str,
        callback: V1ResourceReference | Processor,
        namespace: Optional[str] = None,
        channel: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ):
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        self.api_key = current_server.api_key
        self.orign_host = current_server.server

        if isinstance(callback, Processor):
            callback = callback.ref()  # type: ignore

        self.name = name
        self.medium = medium
        self.namespace = namespace
        self.channel = channel

        # Base URL for humans API
        self.humans_url = f"{self.orign_host}/v1/humans"

        # Check if human exists or create a new one
        humans = self.get(namespace=namespace, name=name, config=config)

        self.human = next(
            (
                h
                for h in humans
                if h.metadata.name == name and h.metadata.namespace == namespace
            ),
            None,
        )

        if not self.human:
            # Human doesn't exist, create it
            request = V1HumanRequest(
                metadata=V1ResourceMetaRequest(
                    name=name,
                    namespace=namespace,
                ),
                medium=medium,
                channel=channel,
                callback=callback,
            )
            response = requests.post(
                self.humans_url,
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            self.human = V1Human.model_validate(response.json())
            print(
                f"Created human {self.human.metadata.namespace}/{self.human.metadata.name}"
            )
        else:
            # Patch the existing human if details differ or simply ensure it's up-to-date
            update_payload = V1UpdateHumanRequest(
                medium=medium,
                channel=channel,
                callback=callback,
            ).model_dump(exclude_none=True)

            # Only patch if there's something to update
            if update_payload:
                patch_url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}"
                response = requests.patch(
                    patch_url,
                    json=update_payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                response.raise_for_status()
                # Update local human object with potentially updated data
                self.human = V1Human.model_validate(response.json())
                print(
                    f"Patched existing human {self.human.metadata.namespace}/{self.human.metadata.name}"
                )
            else:
                print(
                    f"Found existing human {self.human.metadata.namespace}/{self.human.metadata.name} with matching details."
                )

    def feedback(
        self,
        content: str,
        messages: Optional[Dict[str, Any]] = None,
        images: Optional[List[str]] = None,
        videos: Optional[List[str]] = None,
        wait: bool = False,
    ) -> V1FeedbackItem:
        """
        Request feedback from a human.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/feedback"

        request = V1FeedbackRequest(
            kind="approval",
            request=V1ApprovalRequest(
                content=content,
                images=images,
                videos=videos,
                messages=messages,
            ),
        )

        response = requests.post(
            url,
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        resp = V1FeedbackItem.model_validate(response.json())
        if wait:
            resp = self.get_feedback(resp.feedback_id)
            while resp.response is None:
                print("Waiting for feedback...")
                time.sleep(5)
                resp = self.get_feedback(resp.feedback_id)
        return resp

    def record_response(
        self,
        feedback_id: str,
        content: str,
        approved: bool = False,
        messages: Optional[Dict[str, Any]] = None,
        images: Optional[List[str]] = None,
        videos: Optional[List[str]] = None,
    ) -> dict:
        """
        Record a human's response to a feedback request.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/feedback/{feedback_id}"

        data = V1FeedbackResponse(
            kind="approval",
            response=V1ApprovalResponse(
                content=content,
                images=images,
                videos=videos,
                approved=approved,
                messages=messages,
            ),
        )

        response = requests.post(
            url,
            json=data.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()

    def delete(self) -> dict:
        """
        Delete this human.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}"

        response = requests.delete(
            url,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get(
        cls,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ) -> List[V1Human]:
        """
        Get a list of humans, optionally filtered by namespace and/or name.
        """
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        humans_url = f"{current_server.server}/v1/humans"

        response = requests.get(
            humans_url, headers={"Authorization": f"Bearer {current_server.api_key}"}
        )
        response.raise_for_status()

        humans_response = V1Humans.model_validate(response.json())
        humans = humans_response.humans

        if name:
            humans = [h for h in humans if h.metadata.name == name]

        if namespace:
            humans = [h for h in humans if h.metadata.namespace == namespace]

        return humans

    def get_feedback(
        self,
        feedback_id: str,
        config: Optional[GlobalConfig] = None,
    ) -> V1FeedbackItem:
        """
        Get a list of humans, optionally filtered by namespace and/or name.
        """
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        if not self.human or not self.human.metadata:
            raise ValueError("Human not found")

        feedback_url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/feedback/{feedback_id}"

        response = requests.get(
            feedback_url, headers={"Authorization": f"Bearer {current_server.api_key}"}
        )
        response.raise_for_status()
        feedback_response = V1FeedbackItem.model_validate(response.json())

        return feedback_response

    def send_message(
        self, message: str, config: Optional[GlobalConfig] = None
    ) -> V1HumanMessage:
        """
        Send a message to the human.
        """
        config = config or GlobalConfig.read()
        current_server = config.get_current_server_config()
        if not current_server:
            raise ValueError("No current server config found.")
        if not self.human or not self.human.metadata:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/messages"

        response = requests.post(
            url,
            json={"message": message},
            headers={"Authorization": f"Bearer {current_server.api_key}"},
        )
        response.raise_for_status()
        msg = V1HumanMessage.model_validate(response.json())
        return msg
