import asyncio
import logging
import os

from dotenv import load_dotenv
from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config
from langgraph.checkpoint.memory import InMemorySaver

from agents.common import get_llm, load_prompt, get_adapter_features

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    load_dotenv()

    agent_id, api_key = load_agent_config("orchestrator")
    custom_section = load_prompt("orchestrator")

    adapter = LangGraphAdapter(
        llm=get_llm(),
        checkpointer=InMemorySaver(),
        custom_section=custom_section,
        features=get_adapter_features(),
    )

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
        ws_url=os.getenv("BAND_WS_URL"),
        rest_url=os.getenv("BAND_REST_URL"),
    )

    logger.info("Pipeline Orchestrator agent starting — connected to Band")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())