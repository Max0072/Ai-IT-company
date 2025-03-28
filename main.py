from langgraph.graph import StateGraph, START, END

from config.states import MessagesState

from nodes.product_manager import product_manager_graph
from nodes.project_manager import graph
from nodes.empty import empty_graph


# Build graph
builder = StateGraph(MessagesState)

# Nodes
builder.add_node("product_manager", product_manager_graph)
builder.add_node("project_manager", graph)

builder.add_node("empty_node", empty_graph)

# Edges
# builder.add_edge(START, "product_manager")
# builder.add_edge("product_manager", END)


builder.add_edge(START, "empty_node")
builder.add_edge("empty_node", "project_manager")
builder.add_edge("project_manager", END)

# builder.add_edge(START, "product_manager")
# builder.add_edge("product_manager", "project_manager")
# builder.add_edge("project_manager", END)

# Compile
final_graph = builder.compile()


# View
png_data = final_graph.get_graph().draw_mermaid_png()
with open('./pictures/final_graph.png', 'wb') as f:
    f.write(png_data)

# Run
state = final_graph.invoke({"messages": "Type your message"})

# Print
for m in state['technical_chat']:
    m.pretty_print()
