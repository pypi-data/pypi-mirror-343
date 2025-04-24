# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-unsafe

import os
from typing import Iterator, List, Union

from llama_stack.distribution.library_client import LlamaStackAsLibraryClient
from llama_stack_client.lib.agents.agent import Agent

from llama_stack_client.types import ToolResponseMessage, UserMessage

from llama_stack_client.types.agent_create_params import AgentConfig
from llama_stack_client.types.agents import AgentTurnResponseStreamChunk
from llama_stack_client.types.agents.turn import Turn


MODEL_ID = "meta-llama/Llama-3.1-70B-Instruct"


def get_agent() -> Agent:
    client = LlamaStackAsLibraryClient(
        "together",
        provider_data={"tavily_search_api_key": os.environ["TAVILY_SEARCH_API_KEY"]},
    )
    _ = client.initialize()

    agent_config = AgentConfig(
        model=MODEL_ID,
        instructions="You are a helpful assistant",
        toolgroups=["builtin::websearch"],
        input_shields=[],
        output_shields=[],
        enable_session_persistence=False,
    )
    agent = Agent(client, agent_config)
    return agent


def run_agent(prompt: str) -> Iterator[AgentTurnResponseStreamChunk] | Turn:
    agent = get_agent()
    session_id = agent.create_session("test-session")

    messages: List[Union[UserMessage, ToolResponseMessage]] = [
        UserMessage(role="user", content=prompt),
    ]

    response = agent.create_turn(
        messages=messages,
        session_id=session_id,
        stream=False,
    )

    return response
