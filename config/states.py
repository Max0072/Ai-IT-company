from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage


class MessagesState(TypedDict):
    input: str
    messages: Annotated[list[AnyMessage], add_messages]
    interface_messages: Annotated[list[AnyMessage], add_messages]
    product_description: str
    technical_description: str
    technical_critique: str

    technical_chat: Annotated[list[AnyMessage], add_messages]
    tasks: list[dict[str, str]]
    agent_outputs: list[dict[str, str]]

    validation_results: dict[str, dict[str, str]]
    validation_errors: dict[str, str]

    build_log: str
    build_status: str


class ConversationState(TypedDict):
    current_chat: dict[int, int]
    chat_status: dict[int, str]
    new_messages_from: dict[int, list[int]]
    chat: dict[set[int], Annotated[list[str], add_messages]]

    agent_role: dict[int, str]
