from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from config.states import MessagesState
from config.config import llm
from config.config import logger

from config.prompts import MVP_prompt, project_manager_prompt


def technical_director(state: MessagesState):
    logger.info("In technical director MVP")
    system_message = SystemMessage(
        content=MVP_prompt+project_manager_prompt)

    product_description = HumanMessage(content=state["product_description"], name="product_description")
    msg = [system_message, product_description]

    if "technical_chat" in state:
        chat_history = state["technical_chat"]
        msg = [system_message, product_description, *chat_history]

    response = llm.invoke(msg)

    logger.info("Output new technical description from technical director")
    print(response.content)

    description = response.content
    with open("texts/project_description.md", "w", encoding="utf-8") as file:
        file.write(description)

    return {"technical_description": response.content, "technical_chat": [response.content]}


builder = StateGraph(MessagesState)

builder.add_node("technical_director_MVP", technical_director)

builder.add_edge(START, "technical_director_MVP")
builder.add_edge("technical_director_MVP", END)
project_manager_graph = builder.compile()
