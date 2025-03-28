from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from config.states import MessagesState
from config.config import llm
from config.config import logger
import json



def if_final_description(state: MessagesState) -> Literal["final_description", "user_input"]:
    if "tool_calls" in state["messages"][-1].additional_kwargs:
        return "final_description"
    else:
        return "user_input"


def final_description(description: str):
    """
    takes the final description and sends it to the project manager to start the development process
    """
    logger.info("Final product description printed")
    return None


def user_input(state: MessagesState):
    query = ""
    while query.strip() == "":
        query = input(f"{state['messages'][-1].content}")
    return {"input": query, "messages": [HumanMessage(content=query)]}


tools_for_product = [final_description]
llm_for_product = llm.bind_tools(tools_for_product, parallel_tool_calls=False)
coding_and_role_prompt = "Ты такой-то такой-то, у тебя такие-то задачи"


def product_manager(state: MessagesState):
    system_message = SystemMessage(content=coding_and_role_prompt)

    chat_history = state["messages"]
    user_message = HumanMessage(content=state["input"])
    msg = [system_message, *chat_history, user_message]
    response = llm_for_product.invoke(msg)
    if "tool_calls" in response.additional_kwargs:
        dis = response.additional_kwargs["tool_calls"][0]["function"]["arguments"]
        parsed_args = json.loads(dis)
        description = parsed_args.get("description")
        return {"messages": [response], "product_description": description}
    return {"messages": [response]}


def quit_func(state: MessagesState) -> Literal["product_manager", END]:
    x = state['messages'][-1].content
    if x == "quit" or x == "exit":
        return END
    return "product_manager"


# Build graph
builder = StateGraph(MessagesState)

# Nodes
builder.add_node("product_manager", product_manager)
builder.add_node("user_input", user_input)
builder.add_node("final_description", ToolNode(tools_for_product))
# builder.add_node("final_description", final_description(description=""))


# Speak with product_manager and decide what you want to make
builder.add_edge(START, "user_input")
builder.add_conditional_edges("user_input", quit_func)
builder.add_conditional_edges("product_manager", if_final_description)
builder.add_edge("final_description", END)

# Compile
product_manager_graph = builder.compile()

# View
png_data = product_manager_graph.get_graph().draw_mermaid_png()
with open('./pictures/product_graph.png', 'wb') as f:
    f.write(png_data)
