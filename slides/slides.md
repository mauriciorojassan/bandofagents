---
marp: true
theme: uncover
class: invert
paginate: true
size: 16:9
---

# **Band of Agents**
## Post-Merge Delivery Pipeline

**Track 2: Multi-Agent Software Development**
*Band of Agents Hackathon — June 2026*

---

<!-- _class: lead -->

# The Problem

Code is merged. Now what?

**Documentation goes stale.**
**Testing gets deprioritized.**
**Releases get delayed.**

Existing AI tools handle planning → coding → review.
**Nobody handles what comes after the merge.**

---

<!-- _class: lead -->

# The Solution

**Four specialist agents** that collaborate through Band
to automate the post-merge pipeline:

📦 Documentation → 🧪 QA Strategy → 🚀 Release Coordination

Not a thin wrapper. **Genuine multi-agent coordination.**

---

# The Four Agents

| Agent | Role | Band Interaction |
|---|---|---|
| **Pipeline Orchestrator** | Receives tasks, delegates, tracks progress | `band_lookup_peers`, `band_add_participant`, `band_send_event` |
| **Technical Writer** | Generates docs, README updates, API docs | `@mentions` QA, `band_store_memory` |
| **QA Strategist** | Risk assessment, test plans, edge cases | `@mentions` RC, `band_store_memory` |
| **Release Coordinator** | Changelogs, version bumps, checklists | `band_list_memories`, `@mentions` TW + QA for confirmation |

---

# Pipeline Flow

```
User Task
   │
   ▼
Pipeline Orchestrator ── band_lookup_peers ──┐
   │                                          │
   │  @mentions →                             ▼
   │                               Technical Writer
   │                                    │
   │                                    │  @mentions →
   │                                    ▼
   │                              QA Strategist
   │                                    │
   │                                    │  @mentions →
   │                                    ▼
   │                           Release Coordinator
   │                                    │
   ▼                                    ▼
User ◄────────────── Pipeline Complete ──┘
```

---

# Why This Is Meaningful Band Usage

**Not a thin wrapper** — agents collaborate through Band's platform:

1. **@mention routing** — agents discover and address each other
2. **Dynamic peer discovery** — `band_lookup_peers` at runtime
3. **Room management** — `band_add_participant`, `band_get_participants`
4. **Side rooms** — `band_create_chatroom` for focused discussions
5. **Structured events** — `band_send_event` (type='thought') for reasoning
6. **Organization memories** — `band_store_memory` / `band_list_memories` (best-effort on Pro)
7. **Execution reporting** — full audit trail via `Emit.EXECUTION`

---

# Tech Stack

| Component | Technology | Why |
|---|---|---|
| Agent framework | LangGraph via `band-sdk[langgraph]` | Mature adapter, StateGraph support |
| Collaboration | Band.ai (Pro) | @mentions, discovery, rooms, events |
| LLM | Qwen 2.5 14B (Featherless) | Open, fast, reliable tool calling |
| Fallback LLM | Gemini 2.0 Flash | Free tier, unlimited |
| Runtime | Python 3.13 + uv | Fast, isolated, no global installs |

---

<!-- _class: lead -->

# Live Demo

### Four agents. One chat. Zero manual coordination.

---

# Judging Criteria Mapping

| Criteria | How We Meet It |
|---|---|
| **Application of Technology** | 4 agents collaborating via @mentions, peer discovery, room management, event streams, memory — Band is the collaboration layer, not a notification channel |
| **Presentation** | Clear pipeline: Orchestrator → TW → QA → RC, each agent has a distinct role, each handoff is visible in Band chat |
| **Business Value** | Post-merge pipeline is a real enterprise pain — docs go stale, testing deprioritized, releases delayed |
| **Originality** | Not a chatbot or linear automation — agents discover each other, coordinate, divide work, and confirm before shipping |

---

# What We Learned

- **Qwen 2.5 14B** is the sweet spot: 72B too slow (5-10 min), 7B unreliable tool calls
- **Agent identity must be explicit** — without "YOU ARE X, NOT Y" prompts, models confuse roles
- **Handoff flow must be CRITICAL** in prompts or agents skip steps
- **Band memories require Enterprise** — Pro returns 403; agents gracefully skip
- **Band's adapter deprecations** — `enable_execution_reporting` → `AdapterFeatures(emit={Emit.EXECUTION})`

---

<!-- _class: lead -->

# **Band of Agents**
### Post-merge delivery, automated.

**GitHub:** `github.com/mauriciorojassan/bandofagents`

**Track 2: Multi-Agent Software Development**