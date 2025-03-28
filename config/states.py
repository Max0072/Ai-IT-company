from typing import Annotated, TypedDict, Literal
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage


class MessagesState(TypedDict):
    input: str
    messages: Annotated[list[AnyMessage], add_messages]
    interface_messages: Annotated[list[AnyMessage], add_messages]
    product_description: str
    technical_description: str
    technical_critique: str

    technical_chat: Annotated[list[AnyMessage], add_messages]

