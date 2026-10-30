"""
Knowledge base tools for the CloudiQS Agentic AI Bakery.

Provides search, document retrieval, and category browsing for the
company knowledge base. All data is mock/simulated for demo purposes.
"""

import hashlib
import random
from datetime import datetime, timedelta

from strands import tool

# Mock knowledge base data
_KNOWLEDGE_BASE = {
    "KB-001": {
        "title": "Getting Started with AWS Bedrock Agents",
        "category": "engineering",
        "author": "Sarah Chen",
        "last_updated": "2026-10-15",
        "tags": ["aws", "bedrock", "agents", "getting-started"],
        "snippet": "This guide walks you through setting up your first Amazon Bedrock Agent, including model selection, tool configuration, and deployment to AgentCore.",
        "body": (
            "Amazon Bedrock Agents allow you to build AI-powered applications that can "
            "reason, plan, and take actions using foundation models. This guide covers:\n\n"
            "1. **Prerequisites**: AWS account with Bedrock access, IAM roles, and the "
            "Strands Agents SDK installed.\n\n"
            "2. **Creating Your First Agent**: Use the Strands SDK to define an agent with "
            "a system prompt and tools. Example:\n"
            "```python\nfrom strands import Agent\nagent = Agent(system_prompt='You are a helpful assistant.')\n```\n\n"
            "3. **Adding Tools**: Define custom tools using the @tool decorator to give "
            "your agent capabilities like database queries, API calls, and file operations.\n\n"
            "4. **Deploying to AgentCore**: Package your agent for deployment using the "
            "BedrockAgentCoreApp runtime for production workloads.\n\n"
            "5. **Monitoring**: Use CloudWatch metrics and X-Ray tracing to monitor "
            "agent performance and debug issues."
        ),
    },
    "KB-002": {
        "title": "CloudiQS Employee Onboarding Checklist",
        "category": "hr",
        "author": "Michael Torres",
        "last_updated": "2026-10-01",
        "tags": ["onboarding", "hr", "new-hire", "checklist"],
        "snippet": "Complete checklist for new employee onboarding including IT setup, benefits enrollment, mandatory training, and first-week schedule.",
        "body": (
            "Welcome to CloudiQS! This checklist ensures a smooth onboarding experience.\n\n"
            "**Day 1:**\n"
            "- [ ] Pick up laptop and access badge from IT (Floor 2, Room 201)\n"
            "- [ ] Complete I-9 and tax documents with HR\n"
            "- [ ] Set up corporate email and Slack\n"
            "- [ ] Meet your buddy and team lead\n\n"
            "**Week 1:**\n"
            "- [ ] Complete security awareness training\n"
            "- [ ] Enroll in benefits (health, dental, vision, 401k)\n"
            "- [ ] Set up VPN and development environment\n"
            "- [ ] Review company handbook and policies\n"
            "- [ ] Attend new hire orientation session\n\n"
            "**Month 1:**\n"
            "- [ ] Complete all mandatory compliance training\n"
            "- [ ] 30-day check-in with manager\n"
            "- [ ] Set quarterly goals in Lattice"
        ),
    },
    "KB-003": {
        "title": "VPN Troubleshooting Guide",
        "category": "it_support",
        "author": "David Kumar",
        "last_updated": "2026-10-20",
        "tags": ["vpn", "troubleshooting", "network", "connectivity"],
        "snippet": "Step-by-step troubleshooting guide for VPN connectivity issues including common error codes, DNS resolution problems, and MFA token issues.",
        "body": (
            "If you are experiencing VPN connectivity issues, follow these steps:\n\n"
            "**Step 1: Check Your Internet Connection**\n"
            "Ensure you have a stable internet connection by visiting a public website.\n\n"
            "**Step 2: Verify VPN Client Version**\n"
            "Minimum required version: GlobalProtect 6.2+. Update via Software Center.\n\n"
            "**Step 3: Common Error Codes**\n"
            "- Error 1001: Invalid credentials - reset password via SSO portal\n"
            "- Error 1003: MFA timeout - ensure your authenticator app is synced\n"
            "- Error 2001: DNS resolution failure - flush DNS cache\n"
            "- Error 3001: Certificate expired - contact IT for certificate renewal\n\n"
            "**Step 4: Network-Specific Issues**\n"
            "Some hotel and airport networks block VPN traffic. Try using a mobile "
            "hotspot as an alternative.\n\n"
            "**Still stuck?** Create a ticket with category 'network' for IT support."
        ),
    },
    "KB-004": {
        "title": "Multi-Agent Orchestration Patterns",
        "category": "engineering",
        "author": "Priya Sharma",
        "last_updated": "2026-10-25",
        "tags": ["agents", "orchestration", "patterns", "architecture"],
        "snippet": "Architectural patterns for orchestrating multiple AI agents including supervisor, swarm, pipeline, and hierarchical delegation patterns.",
        "body": (
            "This document describes proven patterns for multi-agent orchestration:\n\n"
            "**1. Supervisor Pattern**\n"
            "A supervisor agent routes requests to specialized worker agents based on "
            "intent classification. Best for: customer service with distinct departments.\n\n"
            "**2. Pipeline Pattern**\n"
            "Agents are chained sequentially, each processing and enriching the data. "
            "Best for: document processing, data transformation workflows.\n\n"
            "**3. Swarm Pattern**\n"
            "Multiple agents work on sub-tasks concurrently and results are aggregated. "
            "Best for: research tasks, parallel data gathering.\n\n"
            "**4. Hierarchical Delegation**\n"
            "A manager agent breaks complex tasks into sub-tasks and delegates to "
            "specialist agents. Best for: complex problem solving, project planning.\n\n"
            "**Implementation with Strands SDK:**\n"
            "Use the Agent class with tool-based delegation. Each sub-agent is exposed "
            "as a tool to the orchestrator agent."
        ),
    },
    "KB-005": {
        "title": "Company Travel and Expense Policy",
        "category": "finance",
        "author": "Lisa Park",
        "last_updated": "2026-09-15",
        "tags": ["travel", "expenses", "policy", "reimbursement"],
        "snippet": "Company policy on business travel, expense reporting, per diem rates, and reimbursement procedures. Updated for FY2026.",
        "body": (
            "**Travel Approval:**\n"
            "All business travel must be pre-approved by your manager in Concur.\n\n"
            "**Per Diem Rates (Domestic):**\n"
            "- Tier 1 cities (NYC, SF, DC): $75/day meals\n"
            "- Tier 2 cities: $60/day meals\n"
            "- All other: $50/day meals\n\n"
            "**Lodging:**\n"
            "Book through the corporate travel portal for negotiated rates. "
            "Maximum: $250/night (Tier 1), $175/night (others).\n\n"
            "**Expense Reporting:**\n"
            "Submit expenses within 30 days via Concur. Receipts required for "
            "all expenses over $25. Reimbursement within 5 business days.\n\n"
            "**Mileage:**\n"
            "Personal vehicle: $0.67/mile (IRS 2026 rate)."
        ),
    },
    "KB-006": {
        "title": "API Rate Limiting and Throttling Best Practices",
        "category": "engineering",
        "author": "James Wilson",
        "last_updated": "2026-10-10",
        "tags": ["api", "rate-limiting", "performance", "best-practices"],
        "snippet": "Guidelines for implementing and handling API rate limits in microservices, including token bucket algorithms, retry strategies, and client-side backoff.",
        "body": (
            "**Rate Limiting Strategy:**\n"
            "We use a token bucket algorithm with per-client and global limits.\n\n"
            "**Default Limits:**\n"
            "- Free tier: 100 requests/minute\n"
            "- Standard: 1,000 requests/minute\n"
            "- Enterprise: 10,000 requests/minute\n\n"
            "**Implementation:**\n"
            "Use AWS API Gateway throttling for edge rate limiting. "
            "Application-level: Redis-based sliding window counters.\n\n"
            "**Client-Side Best Practices:**\n"
            "- Implement exponential backoff with jitter\n"
            "- Cache responses where possible\n"
            "- Use bulk/batch endpoints to reduce request count\n"
            "- Monitor 429 response rates in your dashboards"
        ),
    },
    "KB-007": {
        "title": "Security Incident Response Playbook",
        "category": "security",
        "author": "Alex Thompson",
        "last_updated": "2026-10-22",
        "tags": ["security", "incident-response", "playbook", "compliance"],
        "snippet": "Step-by-step playbook for responding to security incidents including data breaches, unauthorized access, malware, and phishing attacks.",
        "body": (
            "**Severity Classification:**\n"
            "- P1 (Critical): Active data breach, ransomware, compromised admin credentials\n"
            "- P2 (High): Suspected unauthorized access, malware detection\n"
            "- P3 (Medium): Phishing attempt, policy violation\n"
            "- P4 (Low): Failed login attempts, vulnerability scan findings\n\n"
            "**Response Steps:**\n"
            "1. **Identify**: Confirm the incident and classify severity\n"
            "2. **Contain**: Isolate affected systems immediately\n"
            "3. **Eradicate**: Remove the threat\n"
            "4. **Recover**: Restore from clean backups\n"
            "5. **Review**: Post-incident review within 48 hours\n\n"
            "**Escalation:**\n"
            "P1/P2: Page on-call security engineer immediately via PagerDuty.\n"
            "P3/P4: Create security ticket and triage next business day."
        ),
    },
    "KB-008": {
        "title": "Strands Agents SDK Quick Reference",
        "category": "engineering",
        "author": "Sarah Chen",
        "last_updated": "2026-10-28",
        "tags": ["strands", "sdk", "agents", "reference", "tools"],
        "snippet": "Quick reference for the Strands Agents SDK including agent creation, tool definition, conversation management, and deployment patterns.",
        "body": (
            "**Installing Strands SDK:**\n"
            "```bash\npip install strands-agents strands-agents-tools\n```\n\n"
            "**Creating an Agent:**\n"
            "```python\nfrom strands import Agent\n"
            "agent = Agent(\n"
            "    system_prompt='You are a helpful assistant.',\n"
            "    tools=[my_tool_1, my_tool_2]\n"
            ")\nresult = agent('Hello!')\n```\n\n"
            "**Defining Tools:**\n"
            "```python\nfrom strands import tool\n\n"
            "@tool\n"
            "def my_tool(param: str) -> dict:\n"
            "    '''Tool description used by the agent.'''\n"
            "    return {'result': param}\n```\n\n"
            "**AgentCore Deployment:**\n"
            "```python\nfrom bedrock_agentcore.runtime import BedrockAgentCoreApp\n"
            "app = BedrockAgentCoreApp()\n\n"
            "@app.entrypoint\n"
            "def invoke(payload):\n"
            "    return agent(payload['message'])\n```"
        ),
    },
    "KB-009": {
        "title": "Benefits Enrollment Guide FY2026",
        "category": "hr",
        "author": "Michael Torres",
        "last_updated": "2026-09-01",
        "tags": ["benefits", "hr", "health", "401k", "enrollment"],
        "snippet": "Complete guide to employee benefits including health insurance plans, dental, vision, 401k matching, stock options, and wellness programs.",
        "body": (
            "**Open Enrollment Period:** November 1 - November 30, 2026\n\n"
            "**Health Insurance:**\n"
            "- PPO Plan: $150/month employee, $400/family\n"
            "- HDHP + HSA: $80/month employee, $250/family (company contributes $1,500/yr to HSA)\n\n"
            "**Dental & Vision:**\n"
            "- Dental: $25/month (covers 2 cleanings/year, 80% major)\n"
            "- Vision: $10/month (annual exam + $200 frame allowance)\n\n"
            "**401(k):**\n"
            "Company matches 100% up to 4% of salary, plus 50% of next 2%.\n\n"
            "**Other Benefits:**\n"
            "- $50/month wellness stipend\n"
            "- $2,000/year learning & development budget\n"
            "- 20 days PTO + 10 holidays\n"
            "- 12 weeks parental leave"
        ),
    },
    "KB-010": {
        "title": "Data Classification and Handling Policy",
        "category": "security",
        "author": "Alex Thompson",
        "last_updated": "2026-10-05",
        "tags": ["data", "classification", "security", "compliance", "policy"],
        "snippet": "Policy defining data classification levels (Public, Internal, Confidential, Restricted) and handling requirements for each level.",
        "body": (
            "**Classification Levels:**\n\n"
            "**Public**: Marketing materials, blog posts, open-source code.\n"
            "Handling: No restrictions.\n\n"
            "**Internal**: Internal wikis, project plans, meeting notes.\n"
            "Handling: Do not share externally. Store on corporate systems only.\n\n"
            "**Confidential**: Customer data, financial reports, employee records.\n"
            "Handling: Encrypt at rest and in transit. Access on need-to-know basis.\n\n"
            "**Restricted**: Credentials, encryption keys, PII, PHI.\n"
            "Handling: Strong encryption required. Access logged and audited. "
            "Never store in code repositories or chat messages."
        ),
    },
}

_CATEGORIES = {
    "engineering": {"name": "Engineering & Development", "count": 4},
    "hr": {"name": "Human Resources", "count": 2},
    "it_support": {"name": "IT Support & Troubleshooting", "count": 1},
    "finance": {"name": "Finance & Operations", "count": 1},
    "security": {"name": "Security & Compliance", "count": 2},
    "product": {"name": "Product & Strategy", "count": 0},
    "sales": {"name": "Sales & Marketing", "count": 0},
}


@tool
def search_knowledge_base(
    query: str,
    category: str = "all",
    max_results: int = 5,
) -> dict:
    """Search the company knowledge base for articles and documentation.

    Use this tool to find answers to questions about company policies,
    technical documentation, how-to guides, and other internal knowledge.
    Returns ranked results with relevance scores.

    Args:
        query: The search query or question (e.g. "how to set up VPN",
               "travel expense policy", "agent deployment guide").
        category: Filter by category - one of "all", "engineering",
                  "hr", "it_support", "finance", "security", "product", "sales".
        max_results: Maximum number of results to return (1-10, default 5).

    Returns:
        A dict with search results including titles, snippets, relevance
        scores, and document IDs for retrieving full content.
    """
    max_results = max(1, min(max_results, 10))
    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored_results = []

    for doc_id, doc in _KNOWLEDGE_BASE.items():
        if category != "all" and doc["category"] != category:
            continue

        score = 0.0

        title_lower = doc["title"].lower()
        for word in query_words:
            if word in title_lower:
                score += 0.3

        snippet_lower = doc["snippet"].lower()
        for word in query_words:
            if word in snippet_lower:
                score += 0.15

        for tag in doc["tags"]:
            if tag in query_lower or any(w in tag for w in query_words):
                score += 0.2

        body_lower = doc["body"].lower()
        for word in query_words:
            if word in body_lower:
                score += 0.05

        # Clamp and add a small random factor for realism
        if score > 0:
            seed = int(hashlib.md5(f"{query}{doc_id}".encode()).hexdigest()[:6], 16)
            jitter = (seed % 100) / 1000.0
            score = min(score + jitter, 1.0)
            scored_results.append((score, doc_id, doc))

    scored_results.sort(key=lambda x: x[0], reverse=True)
    top_results = scored_results[:max_results]

    results = []
    for score, doc_id, doc in top_results:
        results.append({
            "document_id": doc_id,
            "title": doc["title"],
            "category": doc["category"],
            "snippet": doc["snippet"],
            "relevance_score": round(score, 3),
            "author": doc["author"],
            "last_updated": doc["last_updated"],
            "tags": doc["tags"],
        })

    return {
        "query": query,
        "category_filter": category,
        "total_results": len(results),
        "results": results,
        "message": f"Found {len(results)} result(s) for '{query}'"
                   + (f" in category '{category}'" if category != "all" else "")
                   + ".",
    }


@tool
def get_document(document_id: str) -> dict:
    """Retrieve the full content of a specific knowledge base document.

    Use this tool after searching the knowledge base to get the complete
    content of a document. Provide the document_id from search results.

    Args:
        document_id: The document identifier (e.g. "KB-001").

    Returns:
        A dict with the full document content, metadata, and related articles.
    """
    doc_id = document_id.upper().strip()

    if doc_id not in _KNOWLEDGE_BASE:
        return {
            "found": False,
            "error": f"Document '{document_id}' not found. "
                     "Use search_knowledge_base to find available documents.",
        }

    doc = _KNOWLEDGE_BASE[doc_id]

    # Find related documents in the same category
    related = []
    for other_id, other_doc in _KNOWLEDGE_BASE.items():
        if other_id == doc_id:
            continue
        shared_tags = set(doc["tags"]) & set(other_doc["tags"])
        if shared_tags or other_doc["category"] == doc["category"]:
            related.append({
                "document_id": other_id,
                "title": other_doc["title"],
                "shared_tags": list(shared_tags),
            })
    related = related[:3]

    return {
        "found": True,
        "document_id": doc_id,
        "title": doc["title"],
        "category": doc["category"],
        "author": doc["author"],
        "last_updated": doc["last_updated"],
        "tags": doc["tags"],
        "content": doc["body"],
        "related_documents": related,
        "message": f"Retrieved document: {doc['title']}.",
    }


@tool
def list_categories() -> dict:
    """List all available knowledge base categories with article counts.

    Use this tool to help users browse the knowledge base by topic area
    or to understand what types of information are available.

    Returns:
        A dict with all categories, their descriptions, and article counts.
    """
    categories = []
    for key, cat in _CATEGORIES.items():
        categories.append({
            "category_id": key,
            "name": cat["name"],
            "article_count": cat["count"],
        })

    categories.sort(key=lambda c: c["article_count"], reverse=True)

    total_articles = sum(c["article_count"] for c in categories)

    return {
        "total_categories": len(categories),
        "total_articles": total_articles,
        "categories": categories,
        "message": f"Knowledge base has {total_articles} articles across "
                   f"{len(categories)} categories.",
    }
