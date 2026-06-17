#!/usr/bin/env bash
set -euo pipefail

AGENT="${1:?Usage: ./scripts/run_agent.sh <agent_key>

Available agents:
  tech_writer
  qa_strategist
  release_coordinator

Example:
  ./scripts/run_agent.sh tech_writer}"

export AGENT_KEY="$AGENT"

echo "Starting agent: $AGENT_KEY"
exec uv run python -m agents