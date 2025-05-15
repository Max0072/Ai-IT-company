from langgraph.graph import START, END
from config.config import logger

import os
import subprocess
from langgraph.graph import StateGraph
from config.states import MessagesState


def validate_python(code: str) -> (bool, str):
    """Validation for Python"""
    try:
        compile(code, "<string>", "exec")
        return True, ""
    except Exception as e:
        return False, str(e)


def validate_javascript(code: str) -> (bool, str):
    """Validation for Node.js"""
    try:
        with open("temp_validate.js", "w", encoding="utf-8") as f:
            f.write(code)
        result = subprocess.run(["node", "temp_validate.js"], capture_output=True)
        os.remove("temp_validate.js")
        return result.returncode == 0, result.stderr.decode()
    except Exception as e:
        return False, str(e)


def validate_file(path: str, code: str) -> (bool, str):
    ext = os.path.splitext(path)[-1]
    if ext == ".py":
        return validate_python(code)
    elif ext in [".js", ".jsx"]:
        return validate_javascript(code)
    else:
        return True, ""


def validator_node(state: MessagesState):
    logger.info("In validator node")
    outputs = state["agent_outputs"]
    validation_results = {}
    errors = []
    log_lines = ["\n🔍 Validation Summary:\n"]

    for item in outputs:
        role = item["role"]
        files = (item["result"]).get("files", {})
        print(f"role: {role}")
        agent_valid = True
        agent_errors = []

        for path, content in files.items():
            ok, err = validate_file(path, content)
            if not ok:
                agent_valid = False
                agent_errors.append(f"{path}: {err.strip()}")

        status = "✅ OK" if agent_valid else "❌ FAIL"
        log_lines.append(f"{status} — {role}")

        validation_results[role] = {
            "status": "success" if agent_valid else "failed",
            "errors": agent_errors
        }

        if not agent_valid:
            errors.append({
                "role": role,
                "errors": agent_errors
            })

    logger.info("\n".join(log_lines))

    return {"validation_results": validation_results, "validation_errors": errors}


builder = StateGraph(MessagesState)

builder.add_node("validator", validator_node)

builder.add_edge(START, "validator")
builder.add_edge("validator", END)  # или deploy, или test

validator_graph = builder.compile()
