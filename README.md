# Band of Agents — Post-Merge Delivery Pipeline

Multi-agent software delivery system built for the **Band of Agents Hackathon** (June 12–19, 2026). Three specialized agents collaborate through **Band.ai** to handle what happens *after* code is merged: documentation, test planning, and release coordination.

## The Problem

Existing multi-agent coding tools (like Codeband) cover planning → coding → review. But the post-merge pipeline — documentation, test strategy, release coordination — is still manual. These stages require genuine collaboration between specialists, not just sequential handoffs.

## The Solution

Three LangGraph agents that collaborate through Band's platform:

1. **Technical Writer** — Analyzes code changes and generates/updates documentation (API docs, README, inline docs). Shares documentation conventions via Band organization-scoped memories.

2. **QA Strategist** — Analyzes changes for risk areas and generates test plans. Coordinates with coders for intent clarification via `band_lookup_peers`. Stores risk assessments in Band memories for downstream agents.

3. **Release Coordinator** — Reads stored risk assessments and merge history to generate changelogs, propose semver version bumps, and post release checklists. Confirms documentation and test coverage with the other agents.

## Why This Is Meaningful Band Usage

The collaboration is not a thin wrapper or after-the-workflow notification:

- **@mention routing**: Agents discover and address each other directly — Technical Writer @mentions QA Strategist, QA Strategist @mentions Release Coordinator
- **Dynamic peer discovery**: QA Strategist uses `band_lookup_peers` to find coders for intent clarification
- **Side rooms**: Agents create focused chat rooms for detailed discussions (`band_create_chatroom`)
- **Structured memories**: Risk assessments, documentation conventions, and release decisions persist in Band's organization-scoped memory system
- **Cross-agent context**: Release Coordinator reads QA Strategist's stored risk assessments via `band_list_memories` — not a message, not a prompt, but persistent shared knowledge

## Architecture

```
User Task (code merged)
        │
        ▼
  Technical Writer ─── @mention ──► QA Strategist
        │                                │
        │                          band_lookup_peers
        │                          band_create_chatroom
        │                          band_store_memory (risk assessment)
        │                                │
        │                          @mention ──► Release Coordinator
        │                                             │
        ▼                                      band_list_memories (read risk data)
  Documentation ready                     band_store_memory (release decision)
        │                                        │
        └──────────── @mention ──────────────────┘
                        Release checklist posted
```

## Tech Stack

- **Language**: Python 3.11+
- **Agent framework**: LangGraph (via `band-sdk[langgraph]`)
- **Platform**: Band.ai (Pro plan via BANDHACK26)
- **LLM**: Featherless AI (Llama 3.3 70B) with Gemini fallback
- **Package manager**: uv

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Band.ai account (use promo code `BANDHACK26` for free Pro)
- Featherless AI account (use promo code `BOA26` for $25 free credits)

### Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/bandofagents.git
   cd bandofagents
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Create your `.env` file from the template:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. Create three remote agents on [Band.ai](https://app.band.ai/agents) and update `agent_config.yaml` with your agent IDs and API keys.

5. Verify setup:
   ```bash
   uv run python verify_setup.py
   ```

6. Run each agent in a separate terminal:
   ```bash
   # Terminal 1
   AGENT_KEY=tech_writer uv run python -m agents

   # Terminal 2
   AGENT_KEY=qa_strategist uv run python -m agents

   # Terminal 3
   AGENT_KEY=release_coordinator uv run python -m agents
   ```

7. Open [Band.ai](https://app.band.ai), create a chat room, add all three agents, and @mention the Technical Writer with a task!

### Or use the helper script:

```bash
./scripts/run_agent.sh tech_writer      # Terminal 1
./scripts/run_agent.sh qa_strategist   # Terminal 2
./scripts/run_agent.sh release_coordinator  # Terminal 3
```

## Agent Configuration

Each agent is defined in `agent_config.yaml` (gitignored). The format matches what `band.config.load_agent_config()` expects:

```yaml
tech_writer:
  agent_id: "<uuid-from-band>"
  api_key: "<api-key-from-band>"

qa_strategist:
  agent_id: "<uuid-from-band>"
  api_key: "<api-key-from-band>"

release_coordinator:
  agent_id: "<uuid-from-band>"
  api_key: "<api-key-from-band>"
```

## LLM Configuration

The `agents/common.py` module selects an LLM based on available environment variables:

| Priority | Environment Variable | Provider | Model |
|----------|---------------------|----------|-------|
| 1 | `FEATHERLESS_API_KEY` | Featherless AI | Llama 3.3 70B |
| 2 | `GOOGLE_API_KEY` | Google Gemini | gemini-2.0-flash |
| 3 | `OPENAI_API_KEY` | OpenAI | gpt-4o-mini |

All providers use OpenAI-compatible APIs, so switching is just a matter of which key is set.

## Project Structure

```
bandofagents/
├── .env                          # API keys (gitignored)
├── .env.example                  # Template for .env
├── .gitignore
├── agent_config.yaml             # Band agent credentials (gitignored)
├── pyproject.toml                # Dependencies
├── agents/
│   ├── __init__.py               # Entry point (dispatches by AGENT_KEY)
│   ├── common.py                 # Shared LLM factory and config loader
│   ├── tech_writer.py            # Technical Writer agent
│   ├── qa_strategist.py          # QA Strategist agent
│   └── release_coordinator.py    # Release Coordinator agent
├── prompts/
│   ├── tech_writer.md            # System prompt for Technical Writer
│   ├── qa_strategist.md          # System prompt for QA Strategist
│   └── release_coordinator.md    # System prompt for Release Coordinator
├── scripts/
│   └── run_agent.sh              # Helper to run a specific agent
├── verify_setup.py               # Verify connectivity and configuration
└── README.md
```

## Hackathon Track

**Track 2: Multi-Agent Software Development** — three coding-adjacent agents that collaborate across the post-merge lifecycle.

## License

MIT