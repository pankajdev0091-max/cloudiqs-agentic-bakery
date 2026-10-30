"""
Pydantic models for the CloudiQS Agentic AI Bakery API.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return uuid4().hex[:12]


def _new_session_id() -> str:
    return uuid4().hex


# ---------------------------------------------------------------------------
# Agent configuration
# ---------------------------------------------------------------------------

class AgentConfig(BaseModel):
    """Describes an available agent and its capabilities."""

    id: str = Field(..., description="Unique agent identifier")
    name: str = Field(..., description="Human-readable agent name")
    description: str = Field("", description="What this agent does")
    type: str = Field("general", description="Agent category, e.g. helpdesk, sales")
    system_prompt: str = Field("", description="System prompt used by the agent")
    tools: list[str] = Field(default_factory=list, description="Tool names available to the agent")
    model_id: str = Field(
        "us.anthropic.claude-sonnet-4-20250514",
        description="Bedrock model ID used by the agent",
    )
    status: str = Field("active", description="Agent status: active | inactive | maintenance")


# ---------------------------------------------------------------------------
# Chat messages & request / response
# ---------------------------------------------------------------------------

class ChatMessage(BaseModel):
    """A single message in a conversation."""

    role: str = Field(..., description="Message role: user | assistant | system | tool")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=_utc_now, description="UTC timestamp")
    agent_id: Optional[str] = Field(None, description="Agent that produced this message")


class ChatRequest(BaseModel):
    """Payload sent by the client to chat with an agent."""

    agent_id: str = Field(..., description="Target agent identifier")
    message: str = Field(..., min_length=1, description="User message text")
    session_id: Optional[str] = Field(
        default=None,
        description="Conversation session ID; auto-generated when omitted",
    )
    user_id: Optional[str] = Field(
        default=None,
        description="Optional user identifier for multi-tenant scenarios",
    )

    def get_session_id(self) -> str:
        """Return existing session_id or generate a new one."""
        return self.session_id or _new_session_id()


class ChatResponse(BaseModel):
    """Payload returned after an agent processes a message."""

    message: str = Field(..., description="Agent response text")
    session_id: str = Field(..., description="Conversation session ID")
    agent_id: str = Field(..., description="Agent that produced this response")
    metadata: Optional[dict] = Field(
        default=None,
        description="Extra metadata (tool calls, latency, token counts, etc.)",
    )


# ---------------------------------------------------------------------------
# Conversation history
# ---------------------------------------------------------------------------

class ConversationHistory(BaseModel):
    """Full conversation thread for a session."""

    session_id: str = Field(..., description="Session identifier")
    agent_id: str = Field(..., description="Agent that owns this conversation")
    messages: list[ChatMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

class AgentMetrics(BaseModel):
    """Performance metrics for a single agent."""

    agent_id: str = Field(..., description="Agent identifier")
    total_conversations: int = Field(0, ge=0, description="Total conversations handled")
    avg_response_time: float = Field(0.0, ge=0.0, description="Average response time in seconds")
    satisfaction_rate: float = Field(
        0.0, ge=0.0, le=1.0, description="User satisfaction rate (0-1)"
    )
    success_rate: float = Field(
        0.0, ge=0.0, le=1.0, description="Successful resolution rate (0-1)"
    )
