from typing import Dict, List, Optional

from chatmux import ChatRequest, ChatResponse

from orign import OnlineLLM, ReplayBuffer
from orign.config import GlobalConfig
from orign.zoo.processors.qwen_server import QwenVLServer
from orign.zoo.processors.unlsoth_trainer import UnslothSFT

supported_models = [
    "unsloth/Qwen2.5-VL-3B-Instruct",
    "unsloth/Qwen2.5-VL-3B-Instruct-bnb-4bit",
    "unsloth/Qwen2.5-VL-3B-Instruct-unsloth-bnb-4bit",
    "unsloth/Qwen2.5-VL-7B-Instruct",
    "unsloth/Qwen2.5-VL-7B-Instruct-bnb-4bit",
    "unsloth/Qwen2.5-VL-7B-Instruct-unsloth-bnb-4bit",
    "unsloth/Qwen2.5-VL-14B-Instruct",
    "unsloth/Qwen2.5-VL-32B-Instruct",
    "unsloth/Qwen2.5-VL-32B-Instruct-bnb-4bit",
    "unsloth/Qwen2.5-VL-32B-Instruct-unsloth-bnb-4bit",
    "unsloth/Qwen2.5-VL-72B-Instruct",
    "unsloth/Qwen2.5-VL-72B-Instruct-bnb-4bit",
    "unsloth/Qwen2.5-VL-72B-Instruct-unsloth-bnb-4bit",
]


class QwenVL2_5(OnlineLLM[ChatRequest, ChatResponse, ChatRequest]):
    def __init__(
        self,
        name: str,
        namespace: Optional[str] = None,
        model: str = "unsloth/Qwen2.5-VL-32B-Instruct",
        platform: str = "runpod",
        accelerators: List[str] = ["1:A100_SXM"],
        train_every: Optional[int] = None,
        train_n: Optional[int] = None,
        train_strategy: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
        adapter: Optional[str] = None,
        no_delete: bool = False,
    ):
        if model not in supported_models:
            raise ValueError(
                f"Model {model} is not supported, supported models are: {supported_models}"
            )

        server = QwenVLServer(
            platform=platform,
            accelerators=accelerators,
            model=model,
            namespace=namespace,
        )
        buffer = ReplayBuffer(
            name=name,
            namespace=namespace,
            labels=labels,
            config=config,
        )
        trainer = UnslothSFT(
            platform=platform,
            accelerators=accelerators,
            namespace=namespace,
        )
        train_args = {}

        super().__init__(
            name,
            model,
            server.ref(),
            buffer.ref(),
            trainer.ref(),
            train_args,
            train_every,
            train_n,
            train_strategy,
            namespace,
            labels,
            adapter,
            config,
            no_delete,
        )
