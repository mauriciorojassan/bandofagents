# Band of Agents — Post-Merge Delivery Pipeline

> Multi-agent software delivery system built for the **Band of Agents Hackathon** (June 12–19, 2026). Four specialized agents collaborate through **Band.ai** to handle what happens *after* code is merged: documentation, testing strategy, and release coordination.

## The Problem

Existing multi-agent coding tools cover planning → coding → review. But post-merge work — documentation, test planning, release coordination — is still manual. These stages require **genuine collaboration between specialists**, not just sequential handoffs.

## The Solution

Four LangGraph agents that collaborate through Band's platform:

| Agent | Role | Band Collaboration |
|---|---|---|
| **Pipeline Orchestrator** | Receives user tasks, delegates to specialists, tracks pipeline progress | `band_lookup_peers` to discover agents, `band_add_participant` to invite them, `band_send_event` for coordination reasoning |
| **Technical Writer** | Generates API docs, README updates, inline docstrings from code changes | `@mentions` QA Strategist when docs are ready, `band_store_memory` for doc conventions |
| **QA Strategist** | Analyzes risk areas, generates test plans, assesses severity | `band_lookup_peers` for clarification, `@mentions` Release Coordinator with risk verdict, `band_store_memory` for risk data |
| **Release Coordinator** | Generates changelogs, proposes version bumps, posts release checklists | `band_list_memories` to read QA's stored assessments, `@mentions` TW and QA for confirmation |

## Why This Is Meaningful Band Usage

The collaboration is not a thin wrapper or post-workflow notification:

1. **@mention routing**: Agents discover and address each other directly through Band's chat system
2. **Dynamic peer discovery**: The Orchestrator uses `band_lookup_peers` to find available agents at runtime
3. **Room management**: `band_add_participant` and `band_get_participants` ensure the right agents are present
4. **Side rooms**: `band_create_chatroom` for focused discussions
5. **Structured events**: `band_send_event` (type='thought') shares coordination reasoning
6. **Organization-scoped memories**: `band_store_memory` and `band_list_memories` for cross-agent context persistence (best-effort on Pro plan; full on Enterprise)
7. **Execution reporting**: `enable_execution_reporting` sends tool-use logs back to Band for audit trails

## Architecture

```
User Task
   │
   ▼
Pipeline Orchestrator
   │  band_lookup_peers → discover available agents
   │  band_add_participant → ensure all are in the room
   │  band_send_event (thought) → share coordination plan
   │  @mention Technical Writer ──────────────────────┐
   │                                                    │
   ▼                                                    ▼
Technical Writer ── band_store_memory ──► @mentions QA Strategist
   │                                                    │
   │  Generates:                                       ▼
   │  • API docs                               QA Strategist ── band_store_memory ──► @mentions Release Coordinator
   │  • README sections                                  │
   │  • Inline docstrings                               │  Generates:
   │  • Breaking changes                                 │  • Risk assessment (Low/Medium/High/Critical)
   │                                                     │  • Test plan with edge cases
   │                                                     │  • QA verdict
   │                                                     │
   │                                                     ▼
   │                                            Release Coordinator
   │                                              │  band_list_memories → reads QA's stored risk data
   │                                              │  @mentions TW + QA for confirmation
   │                                              │
   │                                              │  Generates:
   │                                              │  • Changelog (feat/fix/breaking/docs/test)
   │                                              │  • Version bump proposal (semver)
   │                                              │  • Release checklist
   │                                              │
   ▼                                              ▼
User ◄──────────────────────── Pipeline Complete ◄──┘
```

## Tech Stack

| Component | Technology | Why |
|---|---|---|
| **Agent framework** | LangGraph (via `band-sdk[langgraph]`) | Most mature Band adapter, supports StateGraph evolution |
| **Collaboration platform** | Band.ai (Pro plan via BANDHACK26) | Chat rooms, @mention routing, peer discovery, memories, event streams |
| **LLM** | Qwen 2.5 14B Instruct (via Featherless AI) | OpenAI-compatible, ungated, fast enough for real-time demo, $25 free credits |
| **LLM fallback** | Google Gemini 2.0 Flash | Free tier, unlimited, good backup |
| **Package manager** | uv | Fast, isolated venv, no global installs |
| **Language** | Python 3.13 | Band SDK is Python-native |

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Band.ai account (use promo code `BANDHACK26` for free Pro)
- Featherless AI account (use promo code `BOA26` for $25 free credits)

### Setup

1. **Clone and install:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/bandofagents.git
   cd bandofagents
   uv sync
   ```

2. **Configure secrets:**

   ```bash
   cp .env.example .env
   # Edit .env with your Featherless API key
   ```

3. **Create agents on [app.band.ai](https://app.band.ai/agents):**

   Create 4 Remote Agents with these names and descriptions:

   | Agent Name | Description |
   |---|---|
   | Pipeline Orchestrator | Receives user tasks and coordinates the post-merge pipeline. Delegates to Technical Writer, QA Strategist, and Release Coordinator via @mentions and peer discovery. Creates side rooms for focused discussions. |
   | Technical Writer | Generates API docs, README updates, and inline docstrings from code changes. @mentions QA Strategist when docs are ready. |
   | QA Strategist | Analyzes code changes for risk areas and generates test plans. @mentions Release Coordinator with risk verdict. |
   | Release Coordinator | Generates changelogs, proposes version bumps, and posts release checklists. Confirms with Technical Writer and QA Strategist. |

   Enable **Personal Registry Access** and **List in public directory** for each agent.

4. **Copy Agent UUIDs and API Keys** into `agent_config.yaml`:

   ```yaml
   orchestrator:
     agent_id: "<uuid>"
     api_key: "<api-key>"

   tech_writer:
     agent_id: "<uuid>"
     api_key: "<api-key>"

   qa_strategist:
     agent_id: "<uuid>"
     api_key: "<api-key>"

   release_coordinator:
     agent_id: "<uuid>"
     api_key: "<api-key>"
   ```

5. **Verify setup:**

   ```bash
   uv run python verify_setup.py
   ```

   All 4 agents should show `PASS`.

6. **Run the agents** (4 separate terminals):

   ```bash
   AGENT_KEY=orchestrator uv run python -m agents          # Terminal 1
   AGENT_KEY=tech_writer uv run python -m agents             # Terminal 2
   AGENT_KEY=qa_strategist uv run python -m agents          # Terminal 3
   AGENT_KEY=release_coordinator uv run python -m agents     # Terminal 4
   ```

   Or use the helper script:

   ```bash
   ./scripts/run_agent.sh orchestrator
   ./scripts/run_agent.sh tech_writer
   ./scripts/run_agent.sh qa_strategist
   ./scripts/run_agent.sh release_coordinator
   ```

7. **Start the pipeline** on [app.band.ai](https://app.band.ai):

   Create a chat room, add all 4 agents as participants, and send:

   ```
   @Pipeline Orchestrator The authentication module had the following changes merged:
   - Added JWT token generation in auth/login.py
   - New API endpoint POST /api/v1/auth/login
   - Added password hashing with bcrypt
   - Updated User model with last_login field

   Please coordinate the post-merge pipeline.
   ```

## Project Structure

```
bandofagents/
├── .env                              # API keys (gitignored)
├── .env.example                      # Template for .env
├── .gitignore
├── agent_config.yaml                  # Band agent credentials (gitignored)
├── pyproject.toml                    # Dependencies
├── agents/
│   ├── __init__.py                   # Entry point: dispatches by AGENT_KEY env var
│   ├── __main__.py                   # Enables `python -m agents`
│   ├── common.py                     # LLM factory + prompt loader + feature flags
│   ├── orchestrator.py               # Pipeline Orchestrator agent
│   ├── tech_writer.py                # Technical Writer agent
│   ├── qa_strategist.py              # QA Strategist agent
│   └── release_coordinator.py        # Release Coordinator agent
├── prompts/
│   ├── orchestrator.md               # System prompt: coordination, delegation, discovery
│   ├── tech_writer.md                # System prompt: documentation, @mention QA
│   ├── qa_strategist.md              # System prompt: risk assessment, @mention RC
│   └── release_coordinator.md       # System prompt: changelog, version bump, confirmation
├── scripts/
│   └── run_agent.sh                  # Helper: ./scripts/run_agent.sh <agent_key>
├── verify_setup.py                   # Connectivity test for all 4 agents
└── README.md
```

## LLM Configuration

The `agents/common.py` module selects an LLM based on available environment variables:

| Priority | Environment Variable | Provider | Default Model |
|---|---|---|---|
| 1 | `FEATHERLESS_API_KEY` | Featherless AI | Qwen/Qwen2.5-14B-Instruct |
| 2 | `GOOGLE_API_KEY` | Google Gemini | gemini-2.0-flash |
| 3 | `OPENAI_API_KEY` | OpenAI | gpt-4o-mini |

Override the default Featherless model with `FEATHERLESS_MODEL` in `.env`:

```env
FEATHERLESS_MODEL=Qwen/Qwen2.5-14B-Instruct   # Balance of speed and quality (default)
# FEATHERLESS_MODEL=Qwen/Qwen2.5-72B-Instruct  # Maximum quality, slower
# FEATHERLESS_MODEL=Qwen/Qwen2.5-7B-Instruct   # Maximum speed, less reliable tool calls
```

## Hackathon Track

**Track 2: Multi-Agent Software Development** — four agents collaborating across the post-merge lifecycle using Band's @mention routing, peer discovery, room management, and memory APIs.

### Judging Criteria Mapping

| Hackathon Criteria | How We Meet It |
|---|---|
| **3+ agents collaborating through Band** | 4 agents: Orchestrator, Technical Writer, QA Strategist, Release Coordinator |
| **Meaningful Band usage** | @mention routing, `band_lookup_peers` for discovery, `band_add_participant` for room management, `band_send_event` for thought sharing, `band_store_memory`/`band_list_memories` for cross-agent context |
| **Cross-framework collaboration** | All agents use LangGraph, but the architecture allows mixing frameworks (CrewAI, PydanticAI, Anthropic) via different Band adapters |
| **Real enterprise use case** | Post-merge pipeline is a real pain point — most teams manually handle docs, testing, and releases after code is merged |

## License

MIT