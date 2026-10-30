"""
Configuration management for CloudiQS Agentic AI Bakery backend.

Loads settings from environment variables with sensible defaults for demo mode.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # AWS Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")

    # Amazon Bedrock Model IDs
    BEDROCK_MODEL_ID: str = os.getenv(
        "BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-20250514"
    )
    BEDROCK_EMBEDDING_MODEL_ID: str = os.getenv(
        "BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"
    )

    # DynamoDB
    DYNAMODB_TABLE_NAME: str = os.getenv(
        "DYNAMODB_TABLE_NAME", "cloudiqs-conversations"
    )
    DYNAMODB_ENDPOINT_URL: str = os.getenv("DYNAMODB_ENDPOINT_URL", "")

    # S3 Knowledge Base
    S3_KNOWLEDGE_BUCKET: str = os.getenv(
        "S3_KNOWLEDGE_BUCKET", "cloudiqs-knowledge-base"
    )

    # API Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

    # CORS
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:8080"
    ).split(",")

    # Demo / Mock Mode
    # When True, agents return mock responses instead of calling Bedrock.
    # Automatically enabled when the strands SDK is not installed.
    MOCK_MODE: bool = os.getenv("MOCK_MODE", "false").lower() in ("true", "1", "yes")

    # Agent Defaults
    DEFAULT_MAX_TURNS: int = int(os.getenv("DEFAULT_MAX_TURNS", "10"))
    DEFAULT_TEMPERATURE: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
