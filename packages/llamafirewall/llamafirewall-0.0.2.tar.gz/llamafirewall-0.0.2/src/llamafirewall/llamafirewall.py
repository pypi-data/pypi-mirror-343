# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

import asyncio

import logging

from typing import Callable, Type

from typing_extensions import Self

from .llamafirewall_data_types import (
    Configuration,
    Message,
    PREDEFINED_USE_CASES,
    Role,
    ScanDecision,
    ScannerType,
    ScanResult,
    Trace,
    UseCase,
)

from .scanners import (
    AlignmentCheckScanner,
    CodeSecurityScanner,
    HiddenASCIIScanner,
    PIICheckScanner,
    PromptInjectionScanner,
    Scanner,
)

LOG: logging.Logger = logging.getLogger(__name__)

custom_scanner_registry: dict[str, type[Scanner]] = {}


def register_llamafirewall_scanner(
    scanner_name: str,
) -> Callable[[Type[Scanner]], Type[Scanner]]:
    def decorator(scanner_class: Type[Scanner]) -> Type[Scanner]:
        if not issubclass(scanner_class, Scanner):
            raise ValueError(
                "[LlamaFirewall] Registered class must be a subclass of Scanner"
            )
        custom_scanner_registry[scanner_name] = scanner_class
        return scanner_class

    return decorator


def create_scanner(scanner_type: ScannerType | str) -> Scanner:
    if isinstance(scanner_type, str) and scanner_type in custom_scanner_registry:
        scanner_class = custom_scanner_registry[scanner_type]
        # pyre-ignore[20]: Registered class must be a subclass of Scanner, so it has a constructor with scanner_name as a parameter
        return scanner_class()
    elif isinstance(scanner_type, ScannerType):
        if scanner_type == ScannerType.CODE_SHIELD:
            return CodeSecurityScanner()
        elif scanner_type == ScannerType.HIDDEN_ASCII:
            return HiddenASCIIScanner()
        elif scanner_type == ScannerType.PROMPT_INJECTION:
            return PromptInjectionScanner()
        elif scanner_type == ScannerType.AGENT_ALIGNMENT:
            return AlignmentCheckScanner()
        elif scanner_type == ScannerType.PII_DETECTION:
            return PIICheckScanner()
        else:
            raise ValueError(
                f"[LlamaFirewall] Unsupported scanner type: {scanner_type}"
            )
    else:
        raise ValueError(f"[LlamaFirewall] Unknown scanner type: {scanner_type}")


class LlamaFirewall:
    def __init__(self, scanners: Configuration | None = None) -> None:
        # Default scanners for each Role
        default_scanners = {
            Role.TOOL: [ScannerType.CODE_SHIELD, ScannerType.PROMPT_INJECTION],
            Role.USER: [ScannerType.PROMPT_INJECTION],
            Role.SYSTEM: [],
            Role.ASSISTANT: [ScannerType.CODE_SHIELD],
            Role.MEMORY: [],
        }
        # Use provided scanners or default to all scanners
        self.scanners: Configuration = scanners or default_scanners

    @classmethod
    def from_usecase(cls, usecase: UseCase) -> Self:
        if usecase not in PREDEFINED_USE_CASES:
            raise Warning(f"Usecase: {usecase} is not predefined with any scanners.")
            return cls()  # or some other default behavior
        return cls(scanners=PREDEFINED_USE_CASES[usecase])

    def invoke(
        self,
        input: Message,
        trace: Trace | None = None,
    ) -> ScanResult:
        for scanner_type in self.scanners.get(input.role, []):
            try:
                scanner_instance = create_scanner(scanner_type)
            except ValueError as e:
                return ScanResult(
                    decision=ScanDecision.HUMAN_IN_THE_LOOP_REQUIRED,
                    reason=str(e),
                    score=1.0,
                )
            LOG.debug(
                f"[LlamaFirewall] Scanning with {scanner_instance.name}, for the input {str(input.content)[:20]}"
            )
            scanner_result = asyncio.run(scanner_instance.scan(input, trace))
            if (
                scanner_result.decision == ScanDecision.BLOCK
                or scanner_result.decision == ScanDecision.HUMAN_IN_THE_LOOP_REQUIRED
            ):
                return scanner_result
        return ScanResult(
            decision=ScanDecision.ALLOW,
            reason="default",
            score=0.0,
        )

    async def async_invoke(
        self,
        input: Message,
        trace: Trace | None = None,
    ) -> ScanResult:
        for scanner_type in self.scanners.get(input.role, []):
            try:
                scanner_instance = create_scanner(scanner_type)
            except ValueError as e:
                return ScanResult(
                    decision=ScanDecision.HUMAN_IN_THE_LOOP_REQUIRED,
                    reason=str(e),
                    score=1.0,
                )
            scanner_result = await scanner_instance.scan(input, trace)
            if (
                scanner_result.decision == ScanDecision.BLOCK
                or scanner_result.decision == ScanDecision.HUMAN_IN_THE_LOOP_REQUIRED
            ):
                return scanner_result
        return ScanResult(
            decision=ScanDecision.ALLOW,
            reason="default",
            score=0.0,
        )

    def message_orchestrator(
        self,
        trace: Trace,
    ) -> ScanResult:
        """
        Process the full trace of messages. Return the final scan result.
        """
        scan_result = ScanResult(
            decision=ScanDecision.ALLOW,
            reason="default",
            score=0.0,
        )
        for current_ix, message in enumerate(trace):
            # Create a new trace up to the current message (excluding it)
            past_trace = [msg for ix, msg in enumerate(trace) if ix < current_ix]
            scan_result = self.invoke(message, past_trace if past_trace else None)
            # Single block or human prevents the rest of the conversation from being scanned
            if scan_result.decision == ScanDecision.BLOCK:
                break
            elif scan_result.decision == ScanDecision.HUMAN_IN_THE_LOOP_REQUIRED:
                break
        return scan_result

    def message_orchestrator_build_trace(
        self,
        message: Message,
        stored_trace: Trace | None = None,
    ) -> tuple[ScanResult, Trace]:
        """
        Process a single message, build and maintain a trace over time.

        Args:
            message: The current message to process
            stored_trace: The existing trace of messages (if any)

        Returns:
            A tuple containing:
            - The scan result
            - The updated trace including the current message (if it passed the scan)
        """
        # Initialize trace if None
        if stored_trace is None:
            stored_trace = []

        # Scan the message with the existing trace
        scan_result = self.invoke(message, stored_trace)

        # If the message passes the scan, add it to the trace
        if scan_result.decision == ScanDecision.ALLOW:
            # Create a new trace with the current message added
            updated_trace = stored_trace + [message]
            return scan_result, updated_trace

        # If the message is blocked or requires human review, don't add it to the trace
        return scan_result, stored_trace
