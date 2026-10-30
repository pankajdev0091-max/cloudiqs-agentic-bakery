"""
Agent factory and in-memory stores for the CloudiQS Agentic AI Bakery.

Manages agent creation, registration, conversation history, and metrics tracking.
"""

from typing import Optional

# ---------------------------------------------------------------------------
# In-memory stores (demo only -- swap for DynamoDB / Redis in production)
# ---------------------------------------------------------------------------
CONVERSATIONS: dict = {}
"""session_id -> list[dict] mapping that holds conversation turns."""

AGENT_METRICS: dict = {
    "it-helpdesk": {
        "total_conversations": 142,
        "total_response_time": 142 * 1.2,
        "satisfaction_total": 142 * 0.94,
        "satisfaction_count": 142,
        "success_count": 129,
        "failure_count": 13,
    },
    "sales-assistant": {
        "total_conversations": 89,
        "total_response_time": 89 * 1.8,
        "satisfaction_total": 89 * 0.92,
        "satisfaction_count": 89,
        "success_count": 77,
        "failure_count": 12,
    },
    "customer-service": {
        "total_conversations": 215,
        "total_response_time": 215 * 1.4,
        "satisfaction_total": 215 * 0.96,
        "satisfaction_count": 215,
        "success_count": 200,
        "failure_count": 15,
    },
    "finance-advisor": {
        "total_conversations": 67,
        "total_response_time": 67 * 2.1,
        "satisfaction_total": 67 * 0.90,
        "satisfaction_count": 67,
        "success_count": 59,
        "failure_count": 8,
    },
    "knowledge-base": {
        "total_conversations": 178,
        "total_response_time": 178 * 0.9,
        "satisfaction_total": 178 * 0.95,
        "satisfaction_count": 178,
        "success_count": 167,
        "failure_count": 11,
    },
}
"""Pre-seeded demo metrics per agent.  Updated at runtime by the chat endpoint.

Keys per agent:
- total_conversations: int
- total_response_time: float (cumulative seconds)
- satisfaction_total: float (cumulative rating)
- satisfaction_count: int (number of ratings)
- success_count: int
- failure_count: int
"""

# ---------------------------------------------------------------------------
# Agent registry
# ---------------------------------------------------------------------------
AGENT_REGISTRY: dict = {
    "it-helpdesk": {
        "id": "it-helpdesk",
        "name": "IT Helpdesk Agent",
        "description": (
            "Handles IT support requests including password resets, ticket "
            "management, system status checks, and general technical troubleshooting."
        ),
        "type": "support",
        "system_prompt": "You are an IT Helpdesk AI Agent for CloudiQS...",
        "tools": [
            "create_ticket",
            "check_ticket_status",
            "reset_password",
            "check_system_status",
        ],
        "model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "status": "active",
    },
    "sales-assistant": {
        "id": "sales-assistant",
        "name": "Sales Assistant Agent",
        "description": (
            "Assists the sales team with lead qualification, CRM lookups, "
            "demo scheduling, and product pricing inquiries."
        ),
        "type": "sales",
        "system_prompt": "You are a Sales Assistant AI Agent for CloudiQS...",
        "tools": [
            "lookup_lead",
            "qualify_lead",
            "schedule_demo",
            "get_pricing",
        ],
        "model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "status": "active",
    },
    "customer-service": {
        "id": "customer-service",
        "name": "Customer Service Agent",
        "description": (
            "Provides customer-facing support by combining ticket management "
            "with knowledge base search for fast, accurate resolutions."
        ),
        "type": "support",
        "system_prompt": "You are a Customer Service AI Agent for CloudiQS...",
        "tools": [
            "create_ticket",
            "check_ticket_status",
            "search_knowledge_base",
            "get_document",
        ],
        "model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "status": "active",
    },
    "finance-advisor": {
        "id": "finance-advisor",
        "name": "Finance Advisor Agent",
        "description": (
            "Provides financial analysis including burn-rate calculations, "
            "runway forecasting, revenue projections, and quarterly summaries."
        ),
        "type": "analytics",
        "system_prompt": "You are a Finance Advisor AI Agent for CloudiQS...",
        "tools": [
            "calculate_burn_rate",
            "calculate_runway",
            "get_financial_summary",
            "forecast_revenue",
        ],
        "model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "status": "active",
    },
    "knowledge-base": {
        "id": "knowledge-base",
        "name": "Knowledge Base Agent",
        "description": (
            "Searches and retrieves information from the company knowledge base, "
            "helping employees quickly find policies, procedures, and documentation."
        ),
        "type": "knowledge",
        "system_prompt": "You are a Knowledge Base AI Agent for CloudiQS...",
        "tools": [
            "search_knowledge_base",
            "get_document",
            "list_categories",
        ],
        "model_id": "us.anthropic.claude-sonnet-4-20250514-v1:0",
        "status": "active",
    },
}


# ---------------------------------------------------------------------------
# Agent factory
# ---------------------------------------------------------------------------
class AgentFactory:
    """Factory for creating and managing Strands agents.

    Agents are lazily instantiated on first request and cached for the
    lifetime of the process.
    """

    _agents: dict = {}

    @classmethod
    def get_agent(cls, agent_id: str) -> Optional[object]:
        """Return a cached Strands Agent instance, creating it on first access."""
        if agent_id not in AGENT_REGISTRY:
            return None
        if agent_id not in cls._agents:
            cls._agents[agent_id] = cls._create_agent(agent_id)
        return cls._agents[agent_id]

    @classmethod
    def _create_agent(cls, agent_id: str) -> Optional[object]:
        """Import and invoke the correct creator function for *agent_id*."""
        from backend.agents.it_helpdesk import create_it_helpdesk_agent
        from backend.agents.sales_agent import create_sales_agent
        from backend.agents.customer_service import create_customer_service_agent
        from backend.agents.finance_agent import create_finance_agent
        from backend.agents.knowledge_base import create_knowledge_base_agent

        creators = {
            "it-helpdesk": create_it_helpdesk_agent,
            "sales-assistant": create_sales_agent,
            "customer-service": create_customer_service_agent,
            "finance-advisor": create_finance_agent,
            "knowledge-base": create_knowledge_base_agent,
        }

        creator = creators.get(agent_id)
        if creator is None:
            return None
        return creator()

    @classmethod
    def list_agents(cls) -> list:
        """Return the full list of registered agent configurations."""
        return list(AGENT_REGISTRY.values())

    @classmethod
    def get_agent_config(cls, agent_id: str) -> Optional[dict]:
        """Return the registry entry for a single agent, or ``None``."""
        return AGENT_REGISTRY.get(agent_id)

    @classmethod
    def reset(cls) -> None:
        """Tear down cached agents (useful for tests)."""
        cls._agents.clear()
