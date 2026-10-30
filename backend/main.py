"""
CloudiQS Agentic AI Bakery - FastAPI Backend
=============================================
Demonstrates AWS AgentCore and Strands Agents SDK capabilities
with multiple specialized AI agents, conversation management,
and multi-agent orchestration patterns.
"""

import time
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.models.schemas import (
    AgentConfig,
    AgentMetrics,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ConversationHistory,
)
from backend.agents.base import AgentFactory, CONVERSATIONS, AGENT_METRICS

# ---------------------------------------------------------------------------
# Check whether the Strands Agents SDK is available at runtime.
# When it is not installed we fall back to a fully self-contained mock that
# returns realistic, keyword-aware responses for every agent type.
# ---------------------------------------------------------------------------
try:
    from strands import Agent as _StrandsAgent  # noqa: F401

    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False


# ---------------------------------------------------------------------------
# Mock Agent Router  (used when Strands SDK is not installed)
# ---------------------------------------------------------------------------
class MockAgentRouter:
    """Generate plausible demo responses by pattern-matching on agent type
    and message keywords.  Each response is 3-5 sentences and references the
    tools the real agent would invoke."""

    _RESPONSES: dict[str, dict[str, str]] = {
        "it-helpdesk": {
            "password": (
                "I have initiated a password reset for your account using the "
                "reset_password tool. You should receive a secure reset link at "
                "your registered email within the next two minutes. Please check "
                "your spam folder if you do not see it. Once reset, your new "
                "password must meet our 12-character complexity policy."
            ),
            "ticket": (
                "I have created IT support ticket TKT-2024-04817 on your behalf "
                "using the create_ticket tool. The ticket has been assigned "
                "medium priority and routed to the Infrastructure team. You can "
                "track its progress by asking me to check the ticket status at "
                "any time."
            ),
            "system": (
                "I just ran a check_system_status query against our core "
                "infrastructure. All primary systems - email gateway, SSO "
                "provider, VPN concentrators, and the internal wiki - are "
                "reporting nominal status with 99.97% uptime over the last 30 "
                "days. No planned maintenance windows are currently scheduled."
            ),
            "network": (
                "I have checked our network monitoring dashboard using "
                "check_system_status. Current latency on the corporate WAN is "
                "12 ms with zero packet loss. If you are experiencing "
                "connectivity issues on Wi-Fi, please try forgetting the "
                "'CloudiQS-Corp' SSID and reconnecting - this resolves most "
                "intermittent issues."
            ),
            "install": (
                "I have created software installation request ticket "
                "TKT-2024-04818 via the create_ticket tool with category "
                "'software-install'. Our IT provisioning team typically "
                "processes these within four business hours. You will receive a "
                "notification once the software is ready on your machine."
            ),
            "_default": (
                "I am the IT Helpdesk agent, ready to assist with any "
                "technology issues. I can create support tickets, reset "
                "passwords, check system status, and help troubleshoot network "
                "or software problems. Please describe your issue and I will "
                "route it to the appropriate team right away."
            ),
        },
        "sales-assistant": {
            "pricing": (
                "I have pulled the latest pricing details using the get_pricing "
                "tool. Our Standard tier starts at $499/month and includes up "
                "to 10 agent deployments with 100k API calls. The Professional "
                "tier at $1,299/month adds priority support, custom model "
                "tuning, and unlimited deployments. I can schedule a call with "
                "our solutions team to discuss volume discounts."
            ),
            "demo": (
                "I would be happy to arrange a product demonstration using the "
                "schedule_demo tool. Our demos typically run 30 minutes and "
                "include a live walkthrough of the Agentic AI Bakery platform "
                "with your specific use case. Please share your preferred date "
                "and time and I will send a calendar invitation immediately."
            ),
            "lead": (
                "I have looked up the contact in our CRM using lookup_lead and "
                "found an existing profile with engagement history. The lead "
                "score is currently 72/100 based on recent website visits and "
                "content downloads. I recommend qualifying them further with a "
                "discovery call to understand budget and timeline."
            ),
            "quote": (
                "I can prepare a custom quote for your organization. Based on "
                "the qualify_lead assessment, your requirements align with our "
                "Professional tier. I will generate a formal proposal with "
                "volume pricing, implementation timeline, and SLA guarantees. "
                "Expect the document in your inbox within the hour."
            ),
            "enterprise": (
                "For enterprise deployments, we offer dedicated infrastructure, "
                "custom SLAs, and a named solutions architect. I have flagged "
                "your account for enterprise qualification using qualify_lead "
                "with tier 'enterprise'. Our enterprise team will reach out "
                "within one business day to discuss a tailored package."
            ),
            "_default": (
                "I am the Sales Assistant agent, here to help with pricing "
                "inquiries, demo scheduling, lead management, and proposal "
                "generation. I can look up your account details, qualify "
                "opportunities, and connect you with the right specialist. How "
                "can I help you move forward today?"
            ),
        },
        "customer-service": {
            "help": (
                "I am here to help resolve your concern as quickly as possible. "
                "I have searched our knowledge base using search_knowledge_base "
                "and found several relevant articles that may address your "
                "question. If those do not resolve the issue, I can escalate by "
                "creating a priority support ticket on your behalf."
            ),
            "issue": (
                "I am sorry to hear you are experiencing an issue. I have "
                "logged the details and created support ticket TKT-2024-05102 "
                "using create_ticket with high priority. Our support "
                "engineering team will investigate and provide an update within "
                "two hours. In the meantime, is there anything else I can "
                "assist with?"
            ),
            "complaint": (
                "I sincerely apologize for the inconvenience and I want to "
                "ensure this is resolved to your satisfaction. I have created a "
                "high-priority escalation ticket TKT-2024-05103 using "
                "create_ticket and flagged it for management review. A senior "
                "support representative will contact you within one hour to "
                "discuss a resolution."
            ),
            "return": (
                "I can help you with the return process. I have looked up your "
                "account and recent orders in our system. Our return policy "
                "allows returns within 30 days of purchase with a full refund. "
                "I will generate a prepaid return label and send it to your "
                "email. Please allow 5-7 business days for the refund to "
                "process once we receive the item."
            ),
            "refund": (
                "I have initiated the refund process for your recent "
                "transaction. The refund of the full purchase amount will be "
                "credited back to your original payment method within 5-7 "
                "business days. I have created tracking ticket TKT-2024-05104 "
                "so you can monitor the status. You will also receive a "
                "confirmation email shortly."
            ),
            "_default": (
                "Welcome to CloudiQS Customer Service. I can help with account "
                "inquiries, troubleshooting, returns, refunds, and general "
                "support questions. I have access to our full knowledge base "
                "and can create support tickets when needed. What can I assist "
                "you with today?"
            ),
        },
        "finance-advisor": {
            "burn rate": (
                "I have calculated your burn rate using the calculate_burn_rate "
                "tool. With monthly expenses of $185,000 and revenue of "
                "$120,000, your net burn rate is $65,000 per month. This "
                "represents a 14% improvement from last quarter. I recommend "
                "focusing on reducing infrastructure costs to bring this below "
                "$50,000."
            ),
            "runway": (
                "Based on the calculate_runway analysis, with your current cash "
                "position of $2.4M and a net monthly burn rate of $65,000, your "
                "runway is approximately 36.9 months. This is a healthy "
                "position, but I recommend maintaining at least 18 months of "
                "runway as a buffer. Consider the impact of planned hiring on "
                "this projection."
            ),
            "revenue": (
                "I have retrieved the financial summary using "
                "get_financial_summary. Current quarter revenue stands at "
                "$360,000 with a month-over-month growth rate of 8.2%. Annual "
                "Recurring Revenue has reached $1.44M. The revenue mix is 72% "
                "subscription and 28% professional services, which is trending "
                "toward our 80/20 target."
            ),
            "forecast": (
                "Using the forecast_revenue tool with your current MRR of "
                "$120,000 and 8.2% monthly growth rate, the 12-month projection "
                "shows revenue reaching $308,000/month by year end. Cumulative "
                "revenue over the period would total approximately $2.52M. This "
                "assumes consistent growth - I recommend modeling conservative "
                "and optimistic scenarios as well."
            ),
            "budget": (
                "I have analyzed your budget allocation using "
                "get_financial_summary. Current spend is distributed as follows: "
                "Engineering 45%, Sales & Marketing 25%, Operations 15%, G&A "
                "15%. Your engineering spend ratio is typical for a growth-stage "
                "company. I can run scenario models if you are considering "
                "reallocation."
            ),
            "_default": (
                "I am the Finance Advisor agent, equipped to analyze burn "
                "rates, calculate runway, forecast revenue, and provide "
                "financial summaries. I can help with budgeting, financial "
                "planning, and data-driven decision making. What financial "
                "question can I help you with?"
            ),
        },
        "knowledge-base": {
            "search": (
                "I have searched the knowledge base using search_knowledge_base "
                "and found 4 relevant results. The top match (relevance: 0.94) "
                "is 'Getting Started with Agentic AI Bakery' which covers "
                "initial setup and configuration. I can retrieve the full "
                "document or refine the search with more specific terms."
            ),
            "document": (
                "I have retrieved the requested document using the get_document "
                "tool. The document 'Agent Deployment Guide v2.3' was last "
                "updated on 2024-11-15 and covers deployment procedures, "
                "configuration options, and troubleshooting steps. Shall I "
                "summarize the key sections or look up a specific topic within "
                "it?"
            ),
            "guide": (
                "I found several guides in our knowledge base using "
                "search_knowledge_base. The most relevant are: 'Quick Start "
                "Guide' (beginner), 'Advanced Agent Configuration' "
                "(intermediate), and 'Production Deployment Playbook' "
                "(advanced). Each includes step-by-step instructions with code "
                "examples. Which one would you like me to pull up?"
            ),
            "how to": (
                "Great question - I have searched the knowledge base for "
                "relevant how-to articles using search_knowledge_base. I found "
                "3 matching tutorials with step-by-step instructions. The "
                "highest-rated article walks through the process with "
                "screenshots and code snippets. Would you like me to retrieve "
                "the full article content?"
            ),
            "policy": (
                "I have located the relevant company policy document using "
                "search_knowledge_base with the 'policies' category filter. The "
                "policy was last reviewed and approved on 2024-10-01. I can "
                "provide the full text or summarize the key points. All "
                "policies are also available on the internal wiki under the "
                "Governance section."
            ),
            "_default": (
                "I am the Knowledge Base agent, here to help you find "
                "information across our document repository. I can search "
                "articles, retrieve specific documents, and list available "
                "categories. Our knowledge base contains technical guides, "
                "company policies, FAQs, and product documentation. What would "
                "you like to look up?"
            ),
        },
    }

    @classmethod
    def generate_response(cls, agent_id: str, message: str) -> str:
        """Return a contextual mock response based on agent type and message
        keywords."""
        message_lower = message.lower()
        agent_responses = cls._RESPONSES.get(agent_id, {})

        if not agent_responses:
            return (
                f"I am the {agent_id} agent running in demo mode. I received "
                f"your message and would normally process it using the Strands "
                f"Agents SDK with specialised tools. Please install the "
                f"strands-agents package to enable full agent capabilities."
            )

        # Check each keyword (excluding the _default key)
        for keyword, response in agent_responses.items():
            if keyword != "_default" and keyword in message_lower:
                return response

        return agent_responses.get("_default", "How can I help you today?")


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CloudiQS Agentic AI Bakery",
    description=(
        "A demonstration platform showcasing AWS AgentCore and Strands Agents "
        "SDK capabilities. Features multiple specialised AI agents with custom "
        "tools, conversation management, and multi-agent orchestration."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_metrics(agent_id: str) -> None:
    """Ensure an entry exists in AGENT_METRICS for *agent_id*."""
    if agent_id not in AGENT_METRICS:
        AGENT_METRICS[agent_id] = {
            "total_conversations": 0,
            "total_response_time": 0.0,
            "satisfaction_total": 0.0,
            "satisfaction_count": 0,
            "success_count": 0,
            "failure_count": 0,
        }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    """API information and status."""
    return {
        "name": "CloudiQS Agentic AI Bakery",
        "version": "1.0.0",
        "description": (
            "Multi-agent AI platform powered by AWS AgentCore and Strands "
            "Agents SDK"
        ),
        "strands_sdk_available": STRANDS_AVAILABLE,
        "mode": "live" if STRANDS_AVAILABLE else "demo",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "timestamp": _now_iso(),
        "version": "1.0.0",
        "strands_available": STRANDS_AVAILABLE,
        "mode": "live" if STRANDS_AVAILABLE else "demo",
    }


@app.get("/api/agents", response_model=list[AgentConfig])
async def list_agents():
    """Return a list of all available agent configurations."""
    return AgentFactory.list_agents()


@app.get("/api/agents/{agent_id}", response_model=AgentConfig)
async def get_agent(agent_id: str):
    """Return configuration details for a single agent."""
    agents = AgentFactory.list_agents()
    for agent_cfg in agents:
        if agent_cfg["id"] == agent_id:
            return agent_cfg
    raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to an agent and receive a response.

    When the Strands SDK is installed the request is routed to a real Strands
    Agent.  Otherwise a keyword-aware mock generates a realistic demo response.
    """
    # Validate agent exists
    agent_ids = [a["id"] for a in AgentFactory.list_agents()]
    if request.agent_id not in agent_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{request.agent_id}' not found. "
                   f"Available agents: {', '.join(agent_ids)}",
        )

    session_id = request.session_id or str(uuid.uuid4())
    user_id = request.user_id or "anonymous"

    # Initialise conversation history for this session
    if session_id not in CONVERSATIONS:
        CONVERSATIONS[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "agent_id": request.agent_id,
            "created_at": _now_iso(),
            "messages": [],
        }

    # Record the user message
    user_msg = {
        "role": "user",
        "content": request.message,
        "timestamp": _now_iso(),
        "agent_id": request.agent_id,
    }
    CONVERSATIONS[session_id]["messages"].append(user_msg)

    # Generate the agent response
    start_time = time.time()

    if STRANDS_AVAILABLE:
        try:
            agent = AgentFactory.get_agent(request.agent_id)
            if agent is None:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to initialise agent '{request.agent_id}'",
                )
            result = agent(request.message)
            response_text = str(result)
        except Exception as exc:
            response_text = (
                f"Agent encountered an error: {exc}. "
                "Falling back to demo mode."
            )
            response_text = MockAgentRouter.generate_response(
                request.agent_id, request.message
            )
    else:
        response_text = MockAgentRouter.generate_response(
            request.agent_id, request.message
        )

    elapsed = time.time() - start_time

    # Record the assistant message
    assistant_msg = {
        "role": "assistant",
        "content": response_text,
        "timestamp": _now_iso(),
        "agent_id": request.agent_id,
    }
    CONVERSATIONS[session_id]["messages"].append(assistant_msg)

    # Update metrics
    _ensure_metrics(request.agent_id)
    metrics = AGENT_METRICS[request.agent_id]
    metrics["total_conversations"] += 1
    metrics["total_response_time"] += elapsed
    metrics["success_count"] += 1

    return ChatResponse(
        message=response_text,
        session_id=session_id,
        agent_id=request.agent_id,
        metadata={
            "mode": "live" if STRANDS_AVAILABLE else "demo",
            "response_time_ms": round(elapsed * 1000, 2),
            "timestamp": _now_iso(),
            "user_id": user_id,
        },
    )


@app.get("/api/conversations/{session_id}", response_model=ConversationHistory)
async def get_conversation(session_id: str):
    """Retrieve the full conversation history for a session."""
    if session_id not in CONVERSATIONS:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found",
        )

    conv = CONVERSATIONS[session_id]
    messages = [ChatMessage(**m) for m in conv["messages"]]
    return ConversationHistory(
        session_id=conv["session_id"],
        agent_id=conv.get("agent_id", "unknown"),
        messages=messages,
        created_at=conv["created_at"],
        updated_at=conv["messages"][-1]["timestamp"] if conv["messages"] else conv["created_at"],
    )


@app.get("/api/agents/{agent_id}/metrics", response_model=AgentMetrics)
async def get_agent_metrics(agent_id: str):
    """Return performance metrics for a specific agent."""
    agent_ids = [a["id"] for a in AgentFactory.list_agents()]
    if agent_id not in agent_ids:
        raise HTTPException(
            status_code=404, detail=f"Agent '{agent_id}' not found"
        )

    _ensure_metrics(agent_id)
    raw = AGENT_METRICS[agent_id]

    total = raw["total_conversations"]
    avg_response = (
        raw["total_response_time"] / total if total > 0 else 0.0
    )
    success = raw["success_count"]
    failure = raw["failure_count"]
    success_rate = success / (success + failure) if (success + failure) > 0 else 1.0

    sat_count = raw["satisfaction_count"]
    satisfaction = (
        raw["satisfaction_total"] / sat_count if sat_count > 0 else 0.95
    )

    return AgentMetrics(
        agent_id=agent_id,
        total_conversations=total,
        avg_response_time=round(avg_response, 4),
        satisfaction_rate=round(satisfaction, 4),
        success_rate=round(success_rate, 4),
    )


@app.get("/api/dashboard/stats")
async def dashboard_stats():
    """Aggregate dashboard statistics across all agents and conversations."""
    agents = AgentFactory.list_agents()
    total_agents = len(agents)
    total_conversations = len(CONVERSATIONS)
    total_messages = sum(
        len(c["messages"]) for c in CONVERSATIONS.values()
    )

    # Aggregate metrics across agents
    overall_total = 0
    overall_response_time = 0.0
    overall_success = 0
    overall_failure = 0

    per_agent: list[dict] = []
    for agent_cfg in agents:
        aid = agent_cfg["id"]
        _ensure_metrics(aid)
        raw = AGENT_METRICS[aid]
        t = raw["total_conversations"]
        overall_total += t
        overall_response_time += raw["total_response_time"]
        overall_success += raw["success_count"]
        overall_failure += raw["failure_count"]
        per_agent.append({
            "agent_id": aid,
            "agent_name": agent_cfg["name"],
            "conversations": t,
        })

    avg_response = (
        overall_response_time / overall_total if overall_total > 0 else 0.0
    )
    success_rate = (
        overall_success / (overall_success + overall_failure)
        if (overall_success + overall_failure) > 0
        else 1.0
    )

    return {
        "total_agents": total_agents,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "total_interactions": overall_total,
        "avg_response_time_s": round(avg_response, 4),
        "overall_success_rate": round(success_rate, 4),
        "mode": "live" if STRANDS_AVAILABLE else "demo",
        "agents": per_agent,
        "timestamp": _now_iso(),
    }
