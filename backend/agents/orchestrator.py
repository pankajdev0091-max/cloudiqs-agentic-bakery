"""
Multi-Agent Orchestration Patterns for CloudiQS Agentic AI Bakery.

Demonstrates three Strands Agents multi-agent patterns:
  1. Graph       - Deterministic routing via a directed graph of agent nodes
  2. Swarm       - Autonomous agent-to-agent handoff for collaborative resolution
  3. Agents-as-Tools - Supervisor agent that delegates to specialist sub-agents

Each pattern is wrapped in a factory function that returns a callable
compatible with the AgentCore invoke interface.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Check SDK availability
# ---------------------------------------------------------------------------
from backend.compat import Agent, tool, GraphBuilder, Swarm, STRANDS_AVAILABLE

# ---------------------------------------------------------------------------
# Agent creators (always importable)
# ---------------------------------------------------------------------------
from backend.agents.it_helpdesk import create_it_helpdesk_agent, SYSTEM_PROMPT as IT_PROMPT
from backend.agents.sales_agent import create_sales_agent, SYSTEM_PROMPT as SALES_PROMPT
from backend.agents.customer_service import create_customer_service_agent, SYSTEM_PROMPT as CS_PROMPT
from backend.agents.finance_agent import create_finance_agent, SYSTEM_PROMPT as FINANCE_PROMPT
from backend.agents.knowledge_base import create_knowledge_base_agent, SYSTEM_PROMPT as KB_PROMPT


# ===================================================================
# Pattern 1: GRAPH — Deterministic Router
# ===================================================================
#
# A classifier node inspects the user message and routes to the
# correct specialist node.  The graph enforces that every request
# goes through exactly one specialist — no loops, no ambiguity.
#
#   ┌──────────┐     ┌──────────────┐     ┌──────────┐
#   │ Classify │────▶│  Route Node  │────▶│ Respond  │
#   └──────────┘     └──────────────┘     └──────────┘
#                         │
#           ┌─────────────┼─────────────┐
#           ▼             ▼             ▼
#     IT Helpdesk    Sales Agent    Finance ...
#
# ===================================================================

CLASSIFIER_PROMPT = """\
You are a request classifier for the CloudiQS Agentic AI Bakery platform.

Analyze the user's message and classify it into exactly ONE category:
- "it-helpdesk"       : password resets, IT tickets, system status, technical issues
- "sales-assistant"   : pricing, demos, lead qualification, product inquiries
- "customer-service"  : orders, complaints, returns, refunds, account issues
- "finance-advisor"   : burn rate, runway, revenue, budgets, financial analysis
- "knowledge-base"    : documentation, guides, how-to, API reference, policies

Respond with ONLY the category id string — nothing else.
"""


def create_graph_orchestrator() -> Any:
    """Build a Graph-based multi-agent orchestrator.

    Uses ``strands.multiagent.GraphBuilder`` to wire a classifier node
    to five specialist agent nodes with conditional edges.

    Returns
    -------
    graph
        A compiled Strands Graph that accepts a user message and
        routes it through the correct specialist agent.
    """
    if not STRANDS_AVAILABLE:
        return None

    classifier = Agent(system_prompt=CLASSIFIER_PROMPT)
    it_agent = create_it_helpdesk_agent()
    sales_agent = create_sales_agent()
    cs_agent = create_customer_service_agent()
    finance_agent = create_finance_agent()
    kb_agent = create_knowledge_base_agent()

    def route_fn(state: dict) -> str:
        """Conditional edge function — returns the next node name."""
        classification = state.get("classification", "knowledge-base").strip().lower()
        valid = {"it-helpdesk", "sales-assistant", "customer-service",
                 "finance-advisor", "knowledge-base"}
        return classification if classification in valid else "knowledge-base"

    graph = (
        GraphBuilder()
        .add_node("classifier", classifier)
        .add_node("it-helpdesk", it_agent)
        .add_node("sales-assistant", sales_agent)
        .add_node("customer-service", cs_agent)
        .add_node("finance-advisor", finance_agent)
        .add_node("knowledge-base", kb_agent)
        .add_edge("classifier", route_fn)
        .set_entry_point("classifier")
        .build()
    )

    return graph


# ===================================================================
# Pattern 2: SWARM — Autonomous Agent Handoff
# ===================================================================
#
# Agents in a swarm can autonomously hand off a conversation to a
# peer when they determine the request is outside their expertise.
#
#   IT Agent ◄──────► Sales Agent
#       ▲                  ▲
#       │                  │
#       ▼                  ▼
#   CS Agent ◄──────► Finance Agent
#
# ===================================================================

IT_SWARM_PROMPT = """\
You are the IT Helpdesk specialist in a collaborative agent swarm.
Handle IT support requests: password resets, tickets, system status.

If the user's request is about sales, pricing, or demos — hand off to the Sales agent.
If the user's request is about billing, complaints, or returns — hand off to Customer Service.
If the user's request is about financial analysis or budgets — hand off to Finance.
If the user's request is about documentation or guides — hand off to Knowledge Base.
"""

SALES_SWARM_PROMPT = """\
You are the Sales specialist in a collaborative agent swarm.
Handle sales inquiries: pricing, demos, lead qualification, proposals.

If the user's request is about IT issues or passwords — hand off to IT Helpdesk.
If the user's request is about existing customer complaints — hand off to Customer Service.
If the user's request is about financial metrics or budgets — hand off to Finance.
If the user's request is about documentation lookups — hand off to Knowledge Base.
"""


def create_swarm_orchestrator() -> Any:
    """Build a Swarm-based multi-agent orchestrator.

    Each agent in the swarm is configured to recognize when a request
    falls outside its domain and autonomously hand off to the
    appropriate peer agent.

    Returns
    -------
    Swarm | None
        A Strands Swarm instance, or None if the SDK is unavailable.
    """
    if not STRANDS_AVAILABLE:
        return None

    from backend.tools.ticket_tools import (
        create_ticket, check_ticket_status, reset_password, check_system_status,
    )
    from backend.tools.crm_tools import (
        lookup_lead, qualify_lead, schedule_demo, get_pricing,
    )
    from backend.tools.knowledge_tools import (
        search_knowledge_base, get_document, list_categories,
    )
    from backend.tools.finance_tools import (
        calculate_burn_rate, calculate_runway, get_financial_summary, forecast_revenue,
    )

    it_agent = Agent(
        name="IT-Helpdesk",
        system_prompt=IT_SWARM_PROMPT,
        tools=[create_ticket, check_ticket_status, reset_password, check_system_status],
    )
    sales_agent = Agent(
        name="Sales-Assistant",
        system_prompt=SALES_SWARM_PROMPT,
        tools=[lookup_lead, qualify_lead, schedule_demo, get_pricing],
    )
    cs_agent = Agent(
        name="Customer-Service",
        system_prompt=CS_PROMPT,
        tools=[create_ticket, check_ticket_status, search_knowledge_base, get_document],
    )
    finance_agent = Agent(
        name="Finance-Advisor",
        system_prompt=FINANCE_PROMPT,
        tools=[calculate_burn_rate, calculate_runway, get_financial_summary, forecast_revenue],
    )
    kb_agent = Agent(
        name="Knowledge-Base",
        system_prompt=KB_PROMPT,
        tools=[search_knowledge_base, get_document, list_categories],
    )

    swarm = Swarm(
        agents=[it_agent, sales_agent, cs_agent, finance_agent, kb_agent],
        max_handoffs=3,
        max_iterations=10,
    )

    return swarm


# ===================================================================
# Pattern 3: AGENTS-AS-TOOLS — Supervisor Delegation
# ===================================================================
#
# A supervisor agent uses specialist agents as callable tools.
# The supervisor decides which specialist(s) to invoke, can invoke
# multiple in sequence, and synthesises a unified response.
#
#   ┌───────────────┐
#   │  Supervisor   │
#   │   Agent       │
#   └──────┬────────┘
#          │ calls as tools
#     ┌────┼────┬────┬────┐
#     ▼    ▼    ▼    ▼    ▼
#    IT  Sales  CS  Fin   KB
#
# ===================================================================

SUPERVISOR_PROMPT = """\
You are the CloudiQS Agentic AI Bakery Supervisor — a senior orchestrating agent \
deployed on Amazon Bedrock AgentCore.

You manage a team of five specialist agents, each available as a tool:
  - ask_it_helpdesk   : IT support, passwords, tickets, system status
  - ask_sales         : pricing, demos, lead qualification
  - ask_customer_service : orders, complaints, returns, refunds
  - ask_finance       : burn rate, runway, revenue, budgets
  - ask_knowledge_base : documentation, guides, API reference

Your job:
1. Analyze the user's request to determine which specialist(s) to invoke.
2. Call the appropriate tool(s). You may call multiple if the request spans domains.
3. Synthesise the specialist responses into a single, coherent answer.
4. If a specialist cannot fully resolve the issue, try another or combine insights.

Always explain which specialist(s) you consulted and why.
"""


def create_supervisor_orchestrator() -> Any:
    """Build an Agents-as-Tools supervisor agent.

    Each specialist agent is wrapped in a ``@tool`` function so the
    supervisor can invoke them by name during its reasoning loop.

    Returns
    -------
    Agent | None
        A Strands Agent configured as a supervisor, or None if SDK unavailable.
    """
    if not STRANDS_AVAILABLE:
        return None

    it_agent = create_it_helpdesk_agent()
    sales_agent = create_sales_agent()
    cs_agent = create_customer_service_agent()
    finance_agent = create_finance_agent()
    kb_agent = create_knowledge_base_agent()

    @tool
    def ask_it_helpdesk(query: str) -> str:
        """Delegate a query to the IT Helpdesk specialist agent.

        Args:
            query: The IT support question or request to handle
        """
        result = it_agent(query)
        return str(result)

    @tool
    def ask_sales(query: str) -> str:
        """Delegate a query to the Sales Assistant specialist agent.

        Args:
            query: The sales or pricing question to handle
        """
        result = sales_agent(query)
        return str(result)

    @tool
    def ask_customer_service(query: str) -> str:
        """Delegate a query to the Customer Service specialist agent.

        Args:
            query: The customer support question or complaint to handle
        """
        result = cs_agent(query)
        return str(result)

    @tool
    def ask_finance(query: str) -> str:
        """Delegate a query to the Finance Advisor specialist agent.

        Args:
            query: The financial analysis question to handle
        """
        result = finance_agent(query)
        return str(result)

    @tool
    def ask_knowledge_base(query: str) -> str:
        """Delegate a query to the Knowledge Base specialist agent.

        Args:
            query: The documentation or reference question to look up
        """
        result = kb_agent(query)
        return str(result)

    supervisor = Agent(
        system_prompt=SUPERVISOR_PROMPT,
        tools=[
            ask_it_helpdesk,
            ask_sales,
            ask_customer_service,
            ask_finance,
            ask_knowledge_base,
        ],
    )

    return supervisor


# ===================================================================
# Mock orchestrators (when Strands SDK is not installed)
# ===================================================================

class MockGraphOrchestrator:
    """Simulates Graph-based routing in demo mode."""

    ROUTE_KEYWORDS = {
        "it-helpdesk": ["password", "ticket", "system", "vpn", "install", "network", "login"],
        "sales-assistant": ["pricing", "demo", "enterprise", "plan", "quote", "lead", "buy"],
        "customer-service": ["order", "return", "refund", "complaint", "delivery", "shipping"],
        "finance-advisor": ["burn rate", "runway", "revenue", "forecast", "budget", "expense"],
        "knowledge-base": ["documentation", "guide", "how to", "api", "deploy", "search", "auth"],
    }

    @classmethod
    def classify(cls, message: str) -> str:
        msg = message.lower()
        for agent_id, keywords in cls.ROUTE_KEYWORDS.items():
            if any(kw in msg for kw in keywords):
                return agent_id
        return "knowledge-base"

    @classmethod
    def describe_routing(cls, message: str, agent_id: str) -> str:
        return (
            f"[Graph Orchestrator] Classified request → routed to **{agent_id}** node.\n\n"
            f"Orchestration pattern: **Deterministic Graph**\n"
            f"- Entry node: Classifier\n"
            f"- Routing decision: message keywords matched '{agent_id}' domain\n"
            f"- Specialist node executed: {agent_id}\n\n"
        )


class MockSwarmOrchestrator:
    """Simulates Swarm-based handoff in demo mode."""

    @classmethod
    def describe_handoff(cls, primary: str, secondary: str | None = None) -> str:
        if secondary:
            return (
                f"[Swarm Orchestrator] **{primary}** handled initial request, "
                f"then autonomously handed off to **{secondary}** for domain-specific resolution.\n\n"
                f"Orchestration pattern: **Autonomous Swarm**\n"
                f"- Initial agent: {primary}\n"
                f"- Handoff triggered: request crossed domain boundary\n"
                f"- Receiving agent: {secondary}\n"
                f"- Total handoffs: 1 (max allowed: 3)\n\n"
            )
        return (
            f"[Swarm Orchestrator] **{primary}** resolved the request directly — "
            f"no handoff required.\n\n"
            f"Orchestration pattern: **Autonomous Swarm**\n"
            f"- Handling agent: {primary}\n"
            f"- Handoffs: 0\n\n"
        )


class MockSupervisorOrchestrator:
    """Simulates Agents-as-Tools supervisor in demo mode."""

    @classmethod
    def describe_delegation(cls, specialists: list[str]) -> str:
        tool_calls = "\n".join(f"  - ask_{s.replace('-', '_')}()" for s in specialists)
        return (
            f"[Supervisor Orchestrator] Delegated to {len(specialists)} specialist(s):\n"
            f"{tool_calls}\n\n"
            f"Orchestration pattern: **Agents-as-Tools (Supervisor)**\n"
            f"- Supervisor analyzed request and selected specialist tool(s)\n"
            f"- Specialist responses synthesised into unified answer\n\n"
        )


# ===================================================================
# Unified entry point for the orchestration demo
# ===================================================================

ORCHESTRATION_PATTERNS = {
    "graph": {
        "name": "Graph Router",
        "description": "Deterministic directed graph with classifier → specialist routing",
        "pattern": "graph",
    },
    "swarm": {
        "name": "Autonomous Swarm",
        "description": "Agents autonomously hand off to peers based on domain expertise",
        "pattern": "swarm",
    },
    "supervisor": {
        "name": "Supervisor (Agents-as-Tools)",
        "description": "Supervisor agent delegates to specialists via tool calls",
        "pattern": "supervisor",
    },
}


def get_orchestration_patterns() -> list[dict]:
    """Return metadata for all available orchestration patterns."""
    return list(ORCHESTRATION_PATTERNS.values())
