from langgraph.graph import START, END
from config.config import logger
from langgraph.graph import StateGraph
from config.states import MessagesState


import os
import subprocess


def run_command(command, cwd):
    """Выполняет команду в заданной директории"""
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
        success = result.returncode == 0
        return success, result.stdout + "\n" + result.stderr
    except Exception as e:
        return False, str(e)


def build_project_node(state: MessagesState):
    project_root = "generated_project"
    log_lines = ["🛠️ Build log:\n"]
    success = True

    for role in os.listdir(project_root):
        role_path = os.path.join(project_root, role)
        if not os.path.isdir(role_path):
            continue

        log_lines.append(f"\n🔧 Checking role: {role}")

        # JS/TS project
        if os.path.exists(os.path.join(role_path, "package.json")):
            ok, out = run_command("npm install", role_path)
            log_lines.append(f"[npm install] {'✅ OK' if ok else '❌ FAIL'}\n{out}")
            success = success and ok

        # Python project
        elif os.path.exists(os.path.join(role_path, "requirements.txt")):
            ok, out = run_command("pip install -r requirements.txt", role_path)
            log_lines.append(f"[pip install] {'✅ OK' if ok else '❌ FAIL'}\n{out}")
            success = success and ok

        # Dockerfile
        elif os.path.exists(os.path.join(role_path, "Dockerfile")):
            image_name = f"ai-company-{role}".replace("_", "-")
            ok, out = run_command(f"docker build -t {image_name} .", role_path)
            log_lines.append(f"[docker build] {'✅ OK' if ok else '❌ FAIL'}\n{out}")
            success = success and ok

        # Prisma schema
        elif os.path.exists(os.path.join(role_path, "schema.prisma")):
            ok, out = run_command("npx prisma generate", role_path)
            log_lines.append(f"[prisma generate] {'✅ OK' if ok else '❌ FAIL'}\n{out}")
            success = success and ok

        else:
            log_lines.append("⚠️ No known build files found")


    build_log = "\n".join(log_lines)
    build_status = "success" if success else "failed"

    logger.info(build_log)
    print(f"\n✅ Build finished: {build_status}")
    return {"build_log": build_log, "build_status": build_status}


builder = StateGraph(MessagesState)

builder.add_node("build_project_node", build_project_node)

builder.add_edge(START, "build_project_node")
builder.add_edge("build_project_node", END)  # или deploy, или test

build_project_graph = builder.compile()