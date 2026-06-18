import os
import asyncio
import logging

AGENTS = {
    "orchestrator": "agents.orchestrator",
    "tech_writer": "agents.tech_writer",
    "qa_strategist": "agents.qa_strategist",
    "release_coordinator": "agents.release_coordinator",
}


def main():
    agent_key = os.environ.get("AGENT_KEY")
    if not agent_key:
        raise ValueError(
            f"AGENT_KEY env var required. Choose from: {', '.join(AGENTS)}"
        )
    if agent_key not in AGENTS:
        raise ValueError(
            f"Unknown AGENT_KEY: {agent_key}. Available: {list(AGENTS)}"
        )

    import importlib

    module = importlib.import_module(AGENTS[agent_key])
    asyncio.run(module.main())


if __name__ == "__main__":
    main()