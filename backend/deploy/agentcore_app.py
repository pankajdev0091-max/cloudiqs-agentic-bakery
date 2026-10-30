"""
Amazon Bedrock AgentCore Runtime - Deployment Entry Point
=========================================================

This module demonstrates how to deploy the CloudiQS Agentic AI Bakery
agents onto Amazon Bedrock AgentCore for production-grade, serverless
execution.

AgentCore provides:
  - Managed runtime for Strands agents
  - Automatic scaling and load balancing
  - Built-in observability (CloudWatch, X-Ray)
  - Session and memory management
  - Identity and access control via IAM

Deployment steps (reference):
  1. Package the application with ``agentcore deploy``
  2. AgentCore builds a container image from this entry point
  3. The ``invoke`` function is called for every inbound request
  4. Responses are streamed back to the caller via the AgentCore gateway

Usage::

    # Install the AgentCore CLI
    pip install bedrock-agentcore-cli

    # Deploy from the project root
    agentcore deploy --entry backend/deploy/agentcore_app.py

"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Agent creators  (always importable - they are pure Python)
# ---------------------------------------------------------------------------
from backend.agents.it_helpdesk import create_it_helpdesk_agent
from backend.agents.sales_agent import create_sales_agent
from backend.agents.customer_service import create_customer_service_agent
from backend.agents.finance_agent import create_finance_agent
from backend.agents.knowledge_base import create_knowledge_base_agent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ---------------------------------------------------------------------------
# Agent registry - lazily instantiated on first request
# ---------------------------------------------------------------------------
_AGENT_CREATORS = {
    "it-helpdesk": create_it_helpdesk_agent,
    "sales-assistant": create_sales_agent,
    "customer-service": create_customer_service_agent,
    "finance-advisor": create_finance_agent,
    "knowledge-base": create_knowledge_base_agent,
}

_AGENT_CACHE: dict[str, Any] = {}


def _get_agent(agent_id: str) -> Any:
    """Return a cached Strands Agent instance, creating one if needed."""
    if agent_id not in _AGENT_CACHE:
        creator = _AGENT_CREATORS.get(agent_id)
        if creator is None:
            raise ValueError(
                f"Unknown agent_id '{agent_id}'. "
                f"Available: {list(_AGENT_CREATORS.keys())}"
            )
        _AGENT_CACHE[agent_id] = creator()
        logger.info("Created agent '%s'", agent_id)
    return _AGENT_CACHE[agent_id]


# ===================================================================
# AgentCore entry point
# ===================================================================
#
# The production deployment uses the BedrockAgentCoreApp class from
# the ``bedrock-agentcore`` package.  The pattern is:
#
#   from bedrock_agentcore.runtime import BedrockAgentCoreApp
#   app = BedrockAgentCoreApp()
#
#   @app.entrypoint
#   def invoke(payload, context):
#       ...process the request...
#       return response_dict
#
# Below we provide both the *real* AgentCore wiring (conditionally
# imported) and a standalone fallback so the file remains runnable
# and testable without the AgentCore SDK installed.
# ===================================================================

try:
    from bedrock_agentcore.runtime import BedrockAgentCoreApp  # type: ignore[import-untyped]

    AGENTCORE_AVAILABLE = True
except ImportError:
    AGENTCORE_AVAILABLE = False


def _handle_invoke(payload: dict) -> dict:
    """Shared logic for handling an invoke request regardless of runtime.

    Parameters
    ----------
    payload : dict
        Expected keys:
            - ``agent_id``  (str)  - which agent to invoke
            - ``message``   (str)  - the user message
            - ``session_id`` (str, optional) - conversation session identifier

    Returns
    -------
    dict
        Response with ``message``, ``session_id``, ``agent_id``, and
        ``metadata``.
    """
    agent_id: str = payload.get("agent_id", "it-helpdesk")
    message: str = payload.get("message", "")
    session_id: str = payload.get("session_id", str(uuid.uuid4()))

    if not message:
        return {
            "error": "No message provided in payload",
            "status": "error",
        }

    logger.info(
        "Invoke  agent=%s  session=%s  message_len=%d",
        agent_id,
        session_id,
        len(message),
    )

    agent = _get_agent(agent_id)
    result = agent(message)
    response_text = str(result)

    return {
        "message": response_text,
        "session_id": session_id,
        "agent_id": agent_id,
        "metadata": {
            "runtime": "agentcore" if AGENTCORE_AVAILABLE else "local",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


# ---------------------------------------------------------------------------
# Production path - BedrockAgentCoreApp
# ---------------------------------------------------------------------------
if AGENTCORE_AVAILABLE:
    app = BedrockAgentCoreApp()

    @app.entrypoint  # type: ignore[misc]
    def invoke(payload: dict, context: Any = None) -> dict:
        """AgentCore invoke handler.

        ``context`` carries runtime metadata (request ID, deadline, etc.)
        provided by the AgentCore runtime.  It is unused in this demo but
        available for production instrumentation.
        """
        return _handle_invoke(payload)

# ---------------------------------------------------------------------------
# Local / demo fallback - runnable without AgentCore SDK
# ---------------------------------------------------------------------------
else:
    logger.info(
        "bedrock-agentcore not installed - running in local demo mode. "
        "Install with: pip install bedrock-agentcore"
    )

    def invoke(payload: dict, context: Any = None) -> dict:  # noqa: F811
        """Local fallback that mirrors the AgentCore invoke signature."""
        return _handle_invoke(payload)


# ---------------------------------------------------------------------------
# CLI convenience - allows ``python -m backend.deploy.agentcore_app``
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_payload = {
        "agent_id": "it-helpdesk",
        "message": "I need to reset my email password",
        "session_id": "demo-session-001",
    }
    print("--- AgentCore Local Invocation ---")
    print(f"Payload: {json.dumps(sample_payload, indent=2)}")
    print()
    response = invoke(sample_payload)
    print(f"Response: {json.dumps(response, indent=2)}")
