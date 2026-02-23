
"""
Configuration loader for Azure OpenAI and AutoGen.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

def get_azure_openai_config() -> Dict[str, Any]:
    """
    Loads Azure OpenAI config from environment variables and returns a config dict for AutoGen.
    Raises ValueError if required variables are missing.

    Returns:
        dict: Azure OpenAI config for AutoGen
    """
    load_dotenv()
    required_vars = [
        "OPENAI_API_KEY",
        "OPENAI_API_BASE",
        "OPENAI_API_VERSION",
        "OPENAI_DEPLOYMENT_NAME",
    ]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise ValueError(f"Missing required env vars: {', '.join(missing)}. See .env.example.")

    config = {
        "api_type": os.getenv("OPENAI_API_TYPE", "azure"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "api_base": os.getenv("OPENAI_API_BASE"),
        "api_version": os.getenv("OPENAI_API_VERSION"),
        # For AutoGen, use 'deployment_name' or 'model' depending on version
        "deployment_name": os.getenv("OPENAI_DEPLOYMENT_NAME"),
    }
    # Optionally add model name if present
    model_name = os.getenv("OPENAI_MODEL_NAME")
    if model_name:
        config["model"] = model_name
    return config
