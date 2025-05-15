from langgraph.graph import START, END

from langgraph.graph import StateGraph
from config.states import MessagesState


def autofix_task_generator_node(state: dict) -> dict:
    outputs = state.get("agent_outputs", [])
    errors = state.get("validation_errors", [])
    autofix_tasks = []

    role_to_files = {o["role"]: o["result"]["files"] for o in outputs}

    for e in errors:
        role = e["role"]
        broken_files = e["errors"]

        for err in broken_files:
            if ":" not in err:
                continue
            file_path, error_msg = err.split(":", 1)
            code = role_to_files.get(role, {}).get(file_path.strip())
            if not code:
                continue

            autofix_prompt = f"""
                You are an Autofix Agent. Your task is to fix the following code:
    
                Role: {role}  
                File path: {file_path.strip()}  
                Error: {error_msg.strip()}
    
                Code:
                {code}
    
                Fix the issue without overcorrecting. Keep the original structure intact.
                Output JSON format:
                {{
                  "files": {{
                    "{file_path.strip()}": "<fixed code here>"
                  }},
                  "notes": "<what was fixed and why>"
                }}
                """.strip()

            autofix_tasks.append({
                "role": role,
                "prompt": autofix_prompt
            })

    return {"tasks": autofix_tasks}


builder = StateGraph(MessagesState)

builder.add_node("autofixer", autofix_task_generator_node)

builder.add_edge(START, "autofixer")
builder.add_edge("autofixer", END)

fix_errors_graph = builder.compile()
