import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Try to load from several possible .env locations
possible_env_files = [
    "core/.env.dev",  # Original location
    ".env",           # In project root directory
    ".env.dev",       # Look for dev version in root directory
]

for env_file in possible_env_files:
    if Path(env_file).exists():
        print(f"Loading environment variables from {env_file}")
        load_dotenv(env_file)
        break

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str = Field(default="your_openrouter_api_key")
    OPENROUTER_URL: str = Field(default="https://openrouter.ai/api/v1")
    OPENROUTER_API_PREFIX: str = Field(default="/ai/openrouter")
    OPENROUTER_INTEGRATION_TESTS: bool = Field(default=False)
    OPENROUTER_API_TEST_MODEL: str = Field(default="meta-llama/llama-3.2-1b-instruct:free")
    OPENROUTER_HEADER_TITLE: str = Field(default="OpenRouter-PyClient")
    OPENROUTER_HEADER_REFERER: str = Field(default="https://github.com/mrcodepanda/openrouter-client")

# Singleton instance
settings = Settings()
