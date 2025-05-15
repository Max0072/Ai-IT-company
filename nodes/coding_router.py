from langgraph.graph import START, END
from langchain_core.messages import HumanMessage, SystemMessage
from config.states import MessagesState
from config.config import logger
from config.config import llm
from concurrent.futures import ThreadPoolExecutor
import json
from config.prompts import code_agent_prompt
from langgraph.graph import StateGraph
import os


def write_files(output: dict, root_dir: str = "."):
    files = output.get("files", {})
    for relative_path, content in files.items():
        full_path = os.path.join(root_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Wrote file: {full_path}")

    if "notes" in output:
        print(f"\n📘 Notes from agent:\n{output['notes']}")


def call_coding_agent(task):
    logger.info(f"In call coding agent: {task["role"]}")
    print(task)
    system_message = SystemMessage(content=code_agent_prompt)
    coding_prompt = HumanMessage(content=task["prompt"], name="coding_prompt")
    messages = [system_message, coding_prompt]
    response = llm.invoke(messages)
    output_json = response.content

    try:
        result = json.loads(output_json)
        assert "files" in result
        return {"role": task["role"], "result": result}

    except Exception as e:
        raise ValueError(f"Invalid JSON returned by code agent:\n{output_json}") from e


def code_router_node(state: MessagesState):
    logger.info("In code router node")
    tasks = state["tasks"]
    outputs = []

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        results = executor.map(call_coding_agent, tasks)
        outputs.extend(results)

    for item in outputs:
        role = item["role"]
        result = item["result"]
        write_files(result, root_dir=os.path.join("generated_project", role))

    with open("texts/agents.json", "w", encoding="utf-8") as f:
        json.dump(outputs, f, ensure_ascii=False, indent=2)

    return {"agent_outputs": outputs}


builder = StateGraph(MessagesState)

builder.add_node("code_router", code_router_node)
builder.add_node("join", lambda state: state)

builder.add_edge(START, "code_router")
builder.add_edge("code_router", END)

router_graph = builder.compile()
