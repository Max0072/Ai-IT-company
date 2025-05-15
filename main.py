from langgraph.graph import StateGraph, START, END

from config.states import MessagesState

from typing import Literal
from nodes.product_manager import product_manager_graph
from nodes.project_manager import project_manager_graph
from nodes.team_lead import team_lead_graph
from nodes.coding_router import router_graph
from nodes.validator import validator_graph
from nodes.autofixer import fix_errors_graph
from nodes.builder import build_project_graph


def validation_router_node(state: MessagesState) -> Literal["handle_failure", "build_project"]:
    results = state["validation_results"]
    for role, info in results.items():
        if info["status"] != "success":
            return "handle_failure"
    return "build_project"


# Build graph
builder = StateGraph(MessagesState)

# Nodes
builder.add_node("product_manager", product_manager_graph)
builder.add_node("project_manager", project_manager_graph)
builder.add_node("team_lead", team_lead_graph)
builder.add_node("coding_router", router_graph)
builder.add_node("validator_node", validator_graph)
builder.add_node("handle_failure", fix_errors_graph)
builder.add_node("build_project", build_project_graph)

builder.add_edge(START, "product_manager")
builder.add_edge("product_manager", "project_manager")
builder.add_edge("project_manager", "team_lead")
builder.add_edge("team_lead", "coding_router")
builder.add_edge("coding_router", "validator_node")
builder.add_conditional_edges("validator_node", validation_router_node)
builder.add_edge("handle_failure", "coding_router")
builder.add_edge("build_project", END)

final_graph = builder.compile()

final_state = final_graph.invoke({"messages": "What project do you want to make?"})
