from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from config.states import MessagesState
from config.config import llm
from config.config import logger

from config.prompts import team_lead_prompt
import json


def team_lead(state: MessagesState):
    logger.info("In team lead node")
    system_message = SystemMessage(content=team_lead_prompt)

    technical_description = HumanMessage(content=state["technical_description"], name="technical_description")
    msg = [system_message, technical_description]
    response = llm.invoke(msg)
    output_json = response.content
    logger.info("Outputing prompts from team lead")
    print(response.content)

    description = response.content
    with open("texts/prompts.json", "w", encoding="utf-8") as file:
        file.write(description)

    try:
        tasks = json.loads(output_json)
    except json.JSONDecodeError as e:
        raise ValueError("Tech lead output is not valid JSON") from e

    return {"tasks": tasks["agent_tasks"]}


builder = StateGraph(MessagesState)

builder.add_node("team_lead", team_lead)

builder.add_edge(START, "team_lead")
builder.add_edge( "team_lead", END)

team_lead_graph = builder.compile()


