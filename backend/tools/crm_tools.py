"""
Sales and CRM tools for the CloudiQS Agentic AI Bakery.

Provides lead management, qualification, demo scheduling, and pricing lookup.
All data is mock/simulated for demo purposes.
"""

import hashlib
import random
from datetime import datetime, timedelta

from backend.compat import tool


@tool
def lookup_lead(email: str) -> dict:
    """Look up a lead or contact in the CRM system by email address.

    Use this tool to retrieve information about a prospect or customer,
    including their company, engagement history, and lead score. Helps
    sales reps prepare for calls and understand the prospect's context.

    Args:
        email: The email address of the lead to look up.

    Returns:
        A dict with the lead's profile, company info, engagement history,
        and lead score.
    """
    if not email or "@" not in email:
        return {
            "found": False,
            "error": "Invalid email address format. Please provide a valid email.",
        }

    seed = int(hashlib.md5(email.lower().strip().encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)

    domain = email.split("@")[1]
    local_part = email.split("@")[0]

    companies = {
        "acme.com": ("Acme Corporation", "Manufacturing", "Enterprise", 2500),
        "techstart.io": ("TechStart Inc.", "SaaS / Technology", "Startup", 45),
        "globalbank.com": ("Global Banking Corp", "Financial Services", "Enterprise", 15000),
        "greenleaf.co": ("GreenLeaf Solutions", "Sustainability / CleanTech", "Mid-Market", 350),
        "healthfirst.org": ("HealthFirst Medical", "Healthcare", "Mid-Market", 800),
    }

    if domain in companies:
        company_name, industry, segment, headcount = companies[domain]
    else:
        company_name = domain.split(".")[0].title() + " Corp"
        industry = rng.choice(["Technology", "Finance", "Healthcare", "Retail", "Energy"])
        segment = rng.choice(["Startup", "Mid-Market", "Enterprise"])
        headcount = rng.choice([20, 80, 250, 1200, 5000])

    first_names = ["Alex", "Jordan", "Morgan", "Casey", "Taylor", "Sam", "Pat"]
    last_names = ["Rivera", "Chen", "Williams", "Patel", "Kim", "Murphy", "Singh"]
    name = f"{rng.choice(first_names)} {rng.choice(last_names)}"

    titles = [
        "VP of Engineering", "CTO", "Director of IT", "Head of Cloud",
        "Chief Data Officer", "VP of Operations", "Director of Innovation",
    ]

    statuses = ["new", "contacted", "qualified", "proposal_sent", "negotiation"]
    lead_score = rng.randint(25, 95)
    status = statuses[min(lead_score // 20, len(statuses) - 1)]

    now = datetime.utcnow()
    first_contact = now - timedelta(days=rng.randint(5, 90))
    last_contact = now - timedelta(days=rng.randint(0, 14))

    return {
        "found": True,
        "lead": {
            "email": email,
            "name": name,
            "title": rng.choice(titles),
            "phone": f"+1-555-{rng.randint(100, 999)}-{rng.randint(1000, 9999)}",
            "company": {
                "name": company_name,
                "industry": industry,
                "segment": segment,
                "headcount": headcount,
                "annual_revenue_estimate": f"${headcount * rng.randint(80, 200):,}K",
            },
            "lead_score": lead_score,
            "status": status,
            "source": rng.choice([
                "Inbound - Website", "Webinar Attendee", "Conference Lead",
                "Partner Referral", "LinkedIn Outreach", "Content Download",
            ]),
            "first_contact": first_contact.strftime("%Y-%m-%d"),
            "last_contact": last_contact.strftime("%Y-%m-%d"),
            "interactions": rng.randint(2, 15),
            "notes": [
                f"Interested in AI/ML capabilities for {industry.lower()} use cases.",
                f"Currently evaluating 2-3 vendors. Budget cycle ends Q{rng.randint(1, 4)}.",
                f"Key decision maker. Reports to CEO.",
            ],
        },
        "message": f"Found lead: {name} at {company_name} (Score: {lead_score}/100, "
                   f"Status: {status}).",
    }


@tool
def qualify_lead(
    company_name: str,
    budget_range: str,
    timeline: str,
    use_case: str,
) -> dict:
    """Qualify a sales lead using BANT criteria (Budget, Authority, Need, Timeline).

    Use this tool to assess whether a prospect is a good fit and determine
    the appropriate sales motion. Provides a qualification score and
    recommended next steps.

    Args:
        company_name: The name of the prospect's company.
        budget_range: The prospect's stated budget range (e.g. "$50K-$100K",
                      "$100K-$500K", "$500K+").
        timeline: When the prospect needs a solution (e.g. "this_quarter",
                  "next_quarter", "6_months", "12_months", "evaluating").
        use_case: Description of what the prospect wants to achieve.

    Returns:
        A dict with the qualification score, BANT breakdown, recommendation,
        and suggested next steps.
    """
    budget_scores = {
        "<$10k": 10, "$10k-$50k": 30, "$50k-$100k": 55,
        "$100k-$500k": 75, "$500k+": 95, "$1m+": 100,
    }
    budget_score = 50
    budget_lower = budget_range.lower().replace(" ", "").replace(",", "")
    for key, score in budget_scores.items():
        if key.replace(" ", "") in budget_lower or budget_lower in key.replace(" ", ""):
            budget_score = score
            break
    if any(big in budget_lower for big in ["500", "million", "1m"]):
        budget_score = max(budget_score, 85)
    elif any(med in budget_lower for med in ["100", "200", "300"]):
        budget_score = max(budget_score, 65)

    timeline_scores = {
        "this_quarter": 95, "next_quarter": 80, "this_month": 100,
        "6_months": 55, "6 months": 55, "12_months": 30,
        "12 months": 30, "evaluating": 20, "next_year": 25,
    }
    timeline_lower = timeline.lower().strip()
    timeline_score = timeline_scores.get(timeline_lower, 40)

    need_keywords_high = [
        "automate", "ai", "machine learning", "modernize", "migrate",
        "scale", "security", "compliance", "cost reduction", "efficiency",
    ]
    need_keywords_medium = [
        "improve", "upgrade", "replace", "explore", "evaluate", "integrate",
    ]
    use_case_lower = use_case.lower()
    need_score = 40
    for kw in need_keywords_high:
        if kw in use_case_lower:
            need_score = min(need_score + 20, 100)
    for kw in need_keywords_medium:
        if kw in use_case_lower:
            need_score = min(need_score + 10, 85)

    authority_score = 70  # assumed moderate without more data

    overall_score = int(
        budget_score * 0.30
        + authority_score * 0.20
        + need_score * 0.25
        + timeline_score * 0.25
    )

    if overall_score >= 75:
        recommendation = "Hot Lead - Prioritize immediate engagement"
        next_steps = [
            "Schedule executive-level discovery call within 48 hours.",
            "Prepare customized demo highlighting relevant use cases.",
            "Assign senior AE and solutions architect to the account.",
            "Draft preliminary proposal with ROI estimates.",
        ]
    elif overall_score >= 50:
        recommendation = "Warm Lead - Nurture with targeted content"
        next_steps = [
            "Send personalized case study for their industry.",
            "Schedule product demo within the next 2 weeks.",
            "Add to targeted email nurture campaign.",
            "Follow up on timeline and buying process.",
        ]
    else:
        recommendation = "Cold Lead - Add to long-term nurture track"
        next_steps = [
            "Add to monthly newsletter and content drip.",
            "Invite to upcoming webinar or industry event.",
            "Set reminder to re-engage next quarter.",
            "Share educational content on relevant topics.",
        ]

    return {
        "company_name": company_name,
        "qualification_score": overall_score,
        "recommendation": recommendation,
        "bant_analysis": {
            "budget": {
                "score": budget_score,
                "input": budget_range,
                "assessment": "Strong" if budget_score >= 65 else "Moderate" if budget_score >= 40 else "Weak",
            },
            "authority": {
                "score": authority_score,
                "assessment": "Assumed moderate - verify decision-making authority",
            },
            "need": {
                "score": need_score,
                "input": use_case,
                "assessment": "Strong" if need_score >= 65 else "Moderate" if need_score >= 40 else "Needs development",
            },
            "timeline": {
                "score": timeline_score,
                "input": timeline,
                "assessment": "Urgent" if timeline_score >= 80 else "Active" if timeline_score >= 50 else "Long-term",
            },
        },
        "next_steps": next_steps,
        "message": f"Lead qualification for {company_name}: Score {overall_score}/100. "
                   f"{recommendation}.",
    }


@tool
def schedule_demo(
    contact_email: str,
    preferred_date: str,
    product_interest: str,
) -> dict:
    """Schedule a product demonstration for a prospect.

    Use this tool when a prospect is ready to see the product in action.
    Creates a calendar event, sends invitations, and assigns a solutions
    engineer.

    Args:
        contact_email: Email address of the prospect to invite.
        preferred_date: Preferred date for the demo (e.g. "2026-11-05",
                        "next Tuesday", "this Friday").
        product_interest: Which product or feature the prospect wants to see
                          (e.g. "AI Agents Platform", "Data Analytics Suite").

    Returns:
        A dict with the demo confirmation, meeting link, and logistics.
    """
    if not contact_email or "@" not in contact_email:
        return {
            "success": False,
            "error": "Invalid email address. Please provide a valid contact email.",
        }

    seed = int(hashlib.md5(
        f"{contact_email}{preferred_date}{product_interest}".encode()
    ).hexdigest()[:8], 16)
    rng = random.Random(seed)

    demo_id = f"DEMO-{rng.randint(10000, 99999)}"

    try:
        demo_date = datetime.strptime(preferred_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        demo_date = datetime.utcnow() + timedelta(days=rng.randint(3, 10))

    demo_time = demo_date.replace(
        hour=rng.choice([10, 11, 14, 15, 16]),
        minute=rng.choice([0, 30]),
    )

    solutions_engineers = [
        {"name": "Rachel Foster", "email": "rachel.foster@cloudiqs.com"},
        {"name": "Marcus Lee", "email": "marcus.lee@cloudiqs.com"},
        {"name": "Priya Sharma", "email": "priya.sharma@cloudiqs.com"},
        {"name": "Chris O'Brien", "email": "chris.obrien@cloudiqs.com"},
    ]
    se = rng.choice(solutions_engineers)

    meeting_token = hashlib.md5(demo_id.encode()).hexdigest()[:10]

    return {
        "success": True,
        "demo_id": demo_id,
        "contact_email": contact_email,
        "product_interest": product_interest,
        "scheduled_datetime": demo_time.isoformat() + "Z",
        "duration_minutes": 45,
        "meeting_link": f"https://meet.cloudiqs.com/demo/{meeting_token}",
        "calendar_invite_sent": True,
        "solutions_engineer": se,
        "agenda": [
            "Introduction and discovery (10 min)",
            f"Product walkthrough: {product_interest} (20 min)",
            "Q&A and next steps (15 min)",
        ],
        "preparation_notes": [
            f"Review {contact_email.split('@')[1]} company profile before the call.",
            f"Prepare {product_interest} demo environment with sample data.",
            "Have pricing sheets and case studies ready.",
        ],
        "message": f"Demo {demo_id} scheduled for {demo_time.strftime('%B %d, %Y at %I:%M %p')} UTC. "
                   f"Calendar invite sent to {contact_email}. "
                   f"Solutions Engineer: {se['name']}.",
    }


@tool
def get_pricing(product: str, tier: str = "standard") -> dict:
    """Get pricing information for a CloudiQS product or service.

    Use this tool when a prospect asks about costs, pricing tiers, or
    wants to compare plans. Returns detailed pricing with feature breakdowns.

    Args:
        product: The product to get pricing for (e.g. "ai_agents", "data_platform",
                 "cloud_ops", "security_suite").
        tier: The pricing tier - one of "starter", "standard", "professional",
              or "enterprise".

    Returns:
        A dict with pricing details, features per tier, and volume discounts.
    """
    products = {
        "ai_agents": {
            "name": "CloudiQS AI Agents Platform",
            "tiers": {
                "starter": {
                    "monthly_price": 499,
                    "annual_price": 4990,
                    "features": [
                        "Up to 3 AI agents",
                        "10,000 conversations/month",
                        "Basic analytics dashboard",
                        "Email support",
                        "Community access",
                    ],
                    "limits": {"agents": 3, "conversations_monthly": 10000},
                },
                "standard": {
                    "monthly_price": 1499,
                    "annual_price": 14990,
                    "features": [
                        "Up to 10 AI agents",
                        "50,000 conversations/month",
                        "Advanced analytics & reporting",
                        "Priority email & chat support",
                        "Custom tool integrations",
                        "A/B testing for agent prompts",
                    ],
                    "limits": {"agents": 10, "conversations_monthly": 50000},
                },
                "professional": {
                    "monthly_price": 3999,
                    "annual_price": 39990,
                    "features": [
                        "Up to 50 AI agents",
                        "250,000 conversations/month",
                        "Real-time analytics & monitoring",
                        "24/7 phone & chat support",
                        "Custom model fine-tuning",
                        "Multi-agent orchestration",
                        "SSO & RBAC",
                        "Dedicated success manager",
                    ],
                    "limits": {"agents": 50, "conversations_monthly": 250000},
                },
                "enterprise": {
                    "monthly_price": None,
                    "annual_price": None,
                    "price_note": "Custom pricing - contact sales",
                    "features": [
                        "Unlimited AI agents",
                        "Unlimited conversations",
                        "Custom SLAs",
                        "On-premise deployment option",
                        "Dedicated infrastructure",
                        "Custom model training",
                        "White-glove onboarding",
                        "Executive business reviews",
                        "Advanced security & compliance",
                    ],
                    "limits": {"agents": "unlimited", "conversations_monthly": "unlimited"},
                },
            },
        },
        "data_platform": {
            "name": "CloudiQS Data Analytics Platform",
            "tiers": {
                "starter": {"monthly_price": 299, "annual_price": 2990, "features": ["5 data sources", "Basic dashboards", "Email support"]},
                "standard": {"monthly_price": 999, "annual_price": 9990, "features": ["25 data sources", "Advanced dashboards", "ML insights", "Priority support"]},
                "professional": {"monthly_price": 2499, "annual_price": 24990, "features": ["100 data sources", "Real-time streaming", "Custom ML models", "24/7 support"]},
                "enterprise": {"monthly_price": None, "annual_price": None, "price_note": "Custom pricing", "features": ["Unlimited sources", "Dedicated cluster", "Custom SLA"]},
            },
        },
        "cloud_ops": {
            "name": "CloudiQS Cloud Operations Suite",
            "tiers": {
                "starter": {"monthly_price": 199, "annual_price": 1990, "features": ["10 resources monitored", "Basic alerts", "Email notifications"]},
                "standard": {"monthly_price": 799, "annual_price": 7990, "features": ["100 resources", "Smart alerts", "Incident management", "Slack integration"]},
                "professional": {"monthly_price": 1999, "annual_price": 19990, "features": ["500 resources", "AI-powered anomaly detection", "Auto-remediation", "24/7 NOC"]},
                "enterprise": {"monthly_price": None, "annual_price": None, "price_note": "Custom pricing", "features": ["Unlimited resources", "Multi-cloud", "Custom runbooks"]},
            },
        },
        "security_suite": {
            "name": "CloudiQS Security Suite",
            "tiers": {
                "starter": {"monthly_price": 399, "annual_price": 3990, "features": ["Vulnerability scanning", "Basic compliance checks", "Monthly reports"]},
                "standard": {"monthly_price": 1299, "annual_price": 12990, "features": ["Continuous scanning", "SIEM integration", "Compliance automation", "Weekly reports"]},
                "professional": {"monthly_price": 3499, "annual_price": 34990, "features": ["Threat intelligence", "Incident response", "Pen testing", "SOC integration"]},
                "enterprise": {"monthly_price": None, "annual_price": None, "price_note": "Custom pricing", "features": ["Managed SOC", "Custom compliance", "Dedicated team"]},
            },
        },
    }

    product_key = product.lower().strip().replace(" ", "_").replace("-", "_")

    # Try fuzzy matching
    matched_product = None
    for key in products:
        if key in product_key or product_key in key:
            matched_product = key
            break
    if matched_product is None:
        # Try keyword matching
        for key in products:
            if any(word in product_key for word in key.split("_")):
                matched_product = key
                break

    if matched_product is None:
        return {
            "found": False,
            "message": f"Product '{product}' not found. Available products: "
                       f"{', '.join(products.keys())}.",
            "available_products": list(products.keys()),
        }

    product_data = products[matched_product]
    tier_lower = tier.lower().strip()
    valid_tiers = list(product_data["tiers"].keys())

    if tier_lower not in product_data["tiers"]:
        tier_lower = "standard"

    selected_tier = product_data["tiers"][tier_lower]

    return {
        "found": True,
        "product": product_data["name"],
        "product_key": matched_product,
        "selected_tier": tier_lower,
        "pricing": selected_tier,
        "all_tiers_summary": {
            t: {
                "monthly": data.get("monthly_price"),
                "annual": data.get("annual_price"),
            }
            for t, data in product_data["tiers"].items()
        },
        "volume_discounts": {
            "10_percent": "10+ seats or annual commitment",
            "15_percent": "50+ seats with annual commitment",
            "20_percent": "100+ seats with multi-year agreement",
        },
        "message": f"{product_data['name']} - {tier_lower.title()} tier: "
                   + (
                       f"${selected_tier['monthly_price']}/mo or "
                       f"${selected_tier['annual_price']}/yr."
                       if selected_tier.get("monthly_price")
                       else "Custom pricing - contact sales."
                   ),
    }
