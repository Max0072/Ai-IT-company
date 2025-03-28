from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from config.states import MessagesState
from config.config import llm
from config.config import logger

from config.prompts import MVP_prompt, ISO_documentation


# def if_final_description(state: MessagesState) -> Literal["final_description", "technical_director_MVP"]:
#     if "tool_calls" in state["messages"][-1].additional_kwargs:
#         return "final_description"
#     else:
#         return "technical_director_MVP"
#
#
# def final_description(description: str):
#     """
#     takes the final description and sends it to the project manager to start the development process
#     """
#     logger.info("Final technical description printed")
#     return None
#
#
# tools_for_technical_critic = [final_description]
# llm_for_critic = llm_o1.bind_tools(tools_for_technical_critic, parallel_tool_calls=False)
#
#
# def MVP_technical_critic(state: MessagesState):
#     logger.info("In technical critic MVP")
#     system_message = SystemMessage(
#         content=MVP_prompt+
#                 f"You are a technical critic. "
#                 f"You will be given product description of the project and a technical solution to it."
#                 f"Your goal is to criticize it and"
#                 f"think of what things were not considered and with what solution you do not agree. "
#                 f"Justify your thoughts."
#                 f"Your answer will be sent to the technical manager"
#                 f"and your considerations will be taken into account."
#                 f"If you are satisfied with the technical solution, "
#                 f"send it to your tool called \"final_description\"."
#                 f"Don't criticize too many times")
#
#     product_description = HumanMessage(content=state["product_description"], name="product_description")
#     # technical_description = HumanMessage(content=state["technical_description"], name="technical_description")
#     # msg = [system_message, product_description, technical_description]
#
#     chat_history = state["technical_chat"]
#     msg = [system_message, product_description, *chat_history]
#     response = llm_for_critic.invoke(msg)
#
#     if "tool_calls" in response.additional_kwargs:
#         parsed_args = json.loads(response.additional_kwargs["tool_calls"][0]["function"]["arguments"])
#         description = parsed_args.get("description")
#         return {"technical_description": description, "technical_chat": [response.content]}
#
#     logger.info("The critic came up with the technical critique...")
#     print(response.content)
#     return {"technical_critique": response.content, "technical_chat": [response.content]}





def technical_director_MVP(state: MessagesState):
    logger.info("In technical director MVP")
    system_message = SystemMessage(
        content=MVP_prompt+ISO_documentation)

    # f"You are a technical manager."
    # f"You will be given a product description of the project and "
    # f"your goal is to come up with the technical solution for it. "
    # f"Think of what things you would need to consider and what technologies you would use. "
    # f"At the same time mention things that you would not implement, "
    # f"it will make the technical task more explicit and clear. "
    # f"Reason your choices and make sure that the technical solution is the best for the project."
    # f"Think of what technologies you would use and what architecture you would choose."
    # f"Output everything you came up with"
    # f"Make technical critic."
    # f"Analise it and improve.")

    product_description = HumanMessage(content=state["product_description"], name="product_description")
    msg = [system_message, product_description]

    if "technical_chat" in state:
        chat_history = state["technical_chat"]
        msg = [system_message, product_description, *chat_history]

    # if "technical_description" in state:
    #     previous_technical_description = AIMessage(content=state["technical_description"])
    #     technical_critique = HumanMessage(content=state["technical_critique"], name="technical_critique")
    #     msg += [previous_technical_description, technical_critique]

    response = llm.invoke(msg)

    logger.info("Outputing new technical description from technical director")
    print(response.content)
    return {"technical_description": response.content, "technical_chat": [response.content]}





builder = StateGraph(MessagesState)

builder.add_node("technical_director_MVP", technical_director_MVP)

builder.add_edge(START, "technical_director_MVP")
builder.add_edge( "technical_director_MVP", END)
graph = builder.compile()

# builder = StateGraph(MessagesState)
#
# builder.add_node("technical_director_MVP", technical_director_MVP)
# builder.add_node("MVP_technical_critic", MVP_technical_critic)
# builder.add_node("final_description", ToolNode(tools_for_technical_critic))
#
# builder.add_edge(START, "technical_director_MVP")
# builder.add_edge( "technical_director_MVP", "MVP_technical_critic")
# builder.add_conditional_edges("MVP_technical_critic", if_final_description)
# builder.add_edge("final_description", END)
# graph = builder.compile()

# View
png_data = graph.get_graph().draw_mermaid_png()
with open('./pictures/project_graph.png', 'wb') as f:
    f.write(png_data)

