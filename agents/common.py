import os
import logging

logger = logging.getLogger(__name__)


def get_llm(model_name=None):
    """Create an LLM instance based on available API keys.

    Priority: Featherless AI > Google Gemini > OpenAI.
    Featherless Qwen 14B is reliable for tool calling.
    Gemini Flash as fast fallback when quota is available.
    """
    featherless_key = os.getenv("FEATHERLESS_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if featherless_key:
        from langchain_openai import ChatOpenAI

        base_url = os.getenv(
            "FEATHERLESS_BASE_URL", "https://api.featherless.ai/v1"
        )
        model = model_name or os.getenv("FEATHERLESS_MODEL", "Qwen/Qwen2.5-14B-Instruct")
        logger.info(f"Using Featherless AI LLM: {model}")
        return ChatOpenAI(
            model=model,
            api_key=featherless_key,
            base_url=base_url,
        )

    if google_key:
        from langchain_google_genai import ChatGoogleGenerativeAI

        model = model_name or os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
        logger.info(f"Using Google Gemini LLM: {model}")
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=google_key,
        )

    if openai_key:
        from langchain_openai import ChatOpenAI

        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        model = model_name or "gpt-4o-mini"
        logger.info(f"Using OpenAI LLM: {model}")
        return ChatOpenAI(
            model=model,
            api_key=openai_key,
            base_url=base_url,
        )

    raise ValueError(
        "No LLM API key found. Set FEATHERLESS_API_KEY, GOOGLE_API_KEY, or OPENAI_API_KEY in .env"
    )


def load_prompt(agent_name: str) -> str:
    """Load a system prompt from the prompts/ directory."""
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", f"{agent_name}.md")
    prompt_path = os.path.normpath(prompt_path)
    with open(prompt_path) as f:
        return f.read()


def get_adapter_features():
    """Return AdapterFeatures with MEMORY capability and EXECUTION emit enabled.

    MEMORY capability adds band_store_memory and band_list_memories tools
    to the agent, enabling cross-agent persistent knowledge sharing.
    EXECUTION emit sends tool-use logs back to the Band platform.
    """
    from band import AdapterFeatures, Capability, Emit

    return AdapterFeatures(
        capabilities={Capability.MEMORY},
        emit={Emit.EXECUTION},
    )


def get_adapter_features_safe():
    """Return AdapterFeatures, falling back to execution-only if MEMORY is not available.

    Band memory tools require an Enterprise plan. If the agent gets 403 Forbidden
    on memory API calls, the tools will be available but return errors. The prompts
    instruct agents to use memories as best-effort: try them, but don't fail if they
    return errors.
    """
    from band import AdapterFeatures, Capability, Emit

    return AdapterFeatures(
        capabilities={Capability.MEMORY},
        emit={Emit.EXECUTION},
    )