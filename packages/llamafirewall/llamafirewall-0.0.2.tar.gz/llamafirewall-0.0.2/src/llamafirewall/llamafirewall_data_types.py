# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

from dataclasses import dataclass
from enum import Enum
from typing import List, Mapping, Sequence, TypeAlias


class ScannerType(Enum):
    CODE_SHIELD = "code_shield"
    PROMPT_INJECTION = "prompt_injection"
    AGENT_ALIGNMENT = "agent_alignment"
    HIDDEN_ASCII = "hidden_ascii"
    PII_DETECTION = "pii_detection"


class ScanDecision(Enum):
    ALLOW = "allow"
    HUMAN_IN_THE_LOOP_REQUIRED = "human_in_the_loop_required"
    BLOCK = "block"


class Role(Enum):
    TOOL = "tool"  # tool output
    USER = "user"  # user input
    ASSISTANT = "assistant"  # LLM output
    MEMORY = "memory"
    SYSTEM = "system"  # system input


@dataclass
class ScanResult:
    decision: ScanDecision
    reason: str
    score: float


@dataclass
class Message:
    role: Role
    content: str
    order: int | None = None

    def __str__(self) -> str:
        return f"{self.role}: {self.content}" + (
            f" (order: {self.order})" if self.order else ""
        )


Trace: TypeAlias = List[Message]


Configuration: TypeAlias = Mapping[Role, Sequence[ScannerType | str]]


class UseCase(Enum):
    CHAT_BOT = "chatbot"
    CODING_ASSISTANT = "coding_assistant"


PREDEFINED_USE_CASES: Mapping[UseCase, Configuration] = {
    UseCase.CHAT_BOT: {
        Role.USER: [ScannerType.PROMPT_INJECTION],
        Role.SYSTEM: [ScannerType.PROMPT_INJECTION],
    },
    UseCase.CODING_ASSISTANT: {
        Role.ASSISTANT: [ScannerType.CODE_SHIELD],
        Role.TOOL: [ScannerType.CODE_SHIELD],
    },
}
