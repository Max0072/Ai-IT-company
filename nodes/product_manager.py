from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage
from config.states import MessagesState
from config.config import llm
from config.config import logger
import json

# def product_description(state: MessagesState):
#     return {"product_description": state["messages"][-1].content}


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


def product_manager(state: MessagesState):
    system_message = SystemMessage(
        content=f"You are a product manager of an IT company. "
                f"From time to time you have clients coming to you with their ideas "
                f"and your goal is to find out all the information needed to develop a project based on their needs."
                f"If you feel like there's not enough information, ask the client and get a reply."
                f"Make sure that there is really enough information given, "
                f"because after we will start to develop the project using this inquiry."
                f"To figure out what thing we will not do is equally important as to figure out the thing we will do."
                f"All in all, the product idea have to be explicitly determined."
                f"Finally, if you feel like you got enough information use your tool called \"final_description\", "
                f"summarize the information about the project without losing anything important details"
                f"and send it to your tool \"final_description\"")

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
