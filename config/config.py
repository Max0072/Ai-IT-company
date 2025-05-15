from langchain_openai import ChatOpenAI
import os
import getpass
from dotenv import load_dotenv
import logging

load_dotenv()


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_o3_mini = ChatOpenAI(model="gpt-o3-mini", temperature=0)
llm_o1 = ChatOpenAI(model="gpt-o1", temperature=0)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger("langgraph")

logger.info("Starting LangGraph process")
