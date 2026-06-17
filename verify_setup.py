"""Verify setup: test Band connectivity and LLM configuration for all 3 agents."""

import asyncio
import logging
import os
import sys

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def verify_agent(agent_key: str) -> bool:
    """Verify that a single agent can connect to Band."""
    from band import Agent
    from band.adapters import LangGraphAdapter
    from band.config import load_agent_config
    from langgraph.checkpoint.memory import InMemorySaver

    from agents.common import get_llm, load_prompt

    try:
        agent_id, api_key = load_agent_config(agent_key)
        logger.info(f"  Credentials loaded: agent_id={agent_id[:8]}...")
    except Exception as e:
        logger.error(f"  Failed to load credentials: {e}")
        return False

    try:
        custom_section = load_prompt(agent_key)
        logger.info(f"  Prompt loaded: {len(custom_section)} chars")
    except Exception as e:
        logger.error(f"  Failed to load prompt: {e}")
        return False

    try:
        llm = get_llm()
        logger.info(f"  LLM configured: {llm.__class__.__name__}")
    except Exception as e:
        logger.error(f"  Failed to configure LLM: {e}")
        return False

    try:
        adapter = LangGraphAdapter(
            llm=llm,
            checkpointer=InMemorySaver(),
            custom_section=custom_section,
            enable_execution_reporting=True,
        )
        agent = Agent.create(
            adapter=adapter,
            agent_id=agent_id,
            api_key=api_key,
            ws_url=os.getenv("BAND_WS_URL"),
            rest_url=os.getenv("BAND_REST_URL"),
        )
        await agent.start()
        logger.info(f"  Connected as: {agent.agent_name}")
        await agent.stop()
        logger.info(f"  Disconnected cleanly")
        return True
    except Exception as e:
        logger.error(f"  Connection failed: {e}")
        return False


async def main():
    load_dotenv()

    agents = ["tech_writer", "qa_strategist", "release_coordinator"]
    results = {}

    logger.info("=" * 50)
    logger.info("Band of Agents — Setup Verification")
    logger.info("=" * 50)

    # Check environment variables
    logger.info("\nEnvironment check:")
    env_vars = {
        "BAND_REST_URL": os.getenv("BAND_REST_URL"),
        "BAND_WS_URL": os.getenv("BAND_WS_URL"),
        "FEATHERLESS_API_KEY": "***" if os.getenv("FEATHERLESS_API_KEY") else None,
        "GOOGLE_API_KEY": "***" if os.getenv("GOOGLE_API_KEY") else None,
        "OPENAI_API_KEY": "***" if os.getenv("OPENAI_API_KEY") else None,
    }
    for key, value in env_vars.items():
        status = "OK" if value else "MISSING"
        logger.info(f"  {key}: {status}")

    # Check LLM availability
    llm_available = any(
        os.getenv(k)
        for k in ["FEATHERLESS_API_KEY", "GOOGLE_API_KEY", "OPENAI_API_KEY"]
    )
    if not llm_available:
        logger.error("\nNo LLM API key found! Set FEATHERLESS_API_KEY, GOOGLE_API_KEY, or OPENAI_API_KEY in .env")
        sys.exit(1)

    # Verify each agent
    for agent_key in agents:
        logger.info(f"\nVerifying: {agent_key}")
        results[agent_key] = await verify_agent(agent_key)

    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("Summary:")
    for agent_key, success in results.items():
        status = "PASS" if success else "FAIL"
        logger.info(f"  {agent_key}: {status}")

    all_passed = all(results.values())
    if all_passed:
        logger.info("\nAll agents verified! Ready to run.")
    else:
        logger.error("\nSome agents failed verification. Check errors above.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())