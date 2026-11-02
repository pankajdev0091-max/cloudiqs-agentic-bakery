"""
IT Helpdesk tools for the CloudiQS Agentic AI Bakery.

Provides ticket management, password resets, and system status checks.
All data is mock/simulated for demo purposes.
"""

import hashlib
import random
from datetime import datetime, timedelta

from backend.compat import tool


@tool
def create_ticket(
    title: str,
    description: str,
    priority: str = "medium",
    category: str = "general",
) -> dict:
    """Create a new IT support ticket in the helpdesk system.

    Use this tool when a user needs to report an issue, request a service,
    or log any IT-related problem. The ticket will be assigned to the
    appropriate team based on category and priority.

    Args:
        title: A short summary of the issue (e.g. "Cannot access VPN").
        description: Detailed description of the problem or request.
        priority: Ticket priority level - one of "low", "medium", "high", or "critical".
        category: Issue category - one of "general", "network", "hardware", "software",
                  "access", "security", or "other".

    Returns:
        A dict with the created ticket details including ticket ID and status.
    """
    valid_priorities = {"low", "medium", "high", "critical"}
    if priority not in valid_priorities:
        priority = "medium"

    valid_categories = {
        "general", "network", "hardware", "software", "access", "security", "other"
    }
    if category not in valid_categories:
        category = "general"

    seed = hashlib.md5(f"{title}{description}{datetime.utcnow().isoformat()}".encode()).hexdigest()
    ticket_num = int(seed[:4], 16) % 9000 + 1000
    ticket_id = f"TKT-{ticket_num}"

    now = datetime.utcnow()

    resolution_hours = {
        "critical": 4,
        "high": 8,
        "medium": 24,
        "low": 72,
    }

    team_map = {
        "network": "Network Operations",
        "hardware": "Desktop Support",
        "software": "Application Support",
        "access": "Identity & Access Management",
        "security": "Security Operations Center",
        "general": "General IT Support",
        "other": "General IT Support",
    }

    return {
        "ticket_id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "open",
        "created_at": now.isoformat() + "Z",
        "estimated_resolution": (
            now + timedelta(hours=resolution_hours[priority])
        ).isoformat() + "Z",
        "assigned_team": team_map.get(category, "General IT Support"),
        "assigned_to": None,
        "sla_target_hours": resolution_hours[priority],
        "message": f"Ticket {ticket_id} created successfully. "
                   f"The {team_map.get(category, 'General IT Support')} team "
                   f"will respond within {resolution_hours[priority]} hours.",
    }


@tool
def check_ticket_status(ticket_id: str) -> dict:
    """Check the current status of an existing IT support ticket.

    Use this tool when a user wants to know the progress of a previously
    created ticket. Returns the latest status, assignment info, and updates.

    Args:
        ticket_id: The ticket identifier (e.g. "TKT-1234").

    Returns:
        A dict with the ticket's current status and latest updates.
    """
    if not ticket_id or not ticket_id.startswith("TKT-"):
        return {
            "error": True,
            "message": f"Invalid ticket ID format: '{ticket_id}'. Expected format: TKT-XXXX.",
        }

    seed = int(hashlib.md5(ticket_id.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)

    statuses = ["open", "in_progress", "in_progress", "resolved", "waiting_on_user"]
    status = rng.choice(statuses)

    assignees = [
        "Alex Thompson", "Maria Garcia", "James Wilson",
        "Sarah Chen", "David Kumar", "Emily Rodriguez",
    ]

    priorities = ["low", "medium", "medium", "high", "critical"]
    categories = ["network", "software", "access", "hardware", "general"]

    now = datetime.utcnow()
    created = now - timedelta(hours=rng.randint(2, 72))
    last_update = now - timedelta(minutes=rng.randint(5, 360))

    updates = []
    if status in ("in_progress", "resolved", "waiting_on_user"):
        updates.append({
            "timestamp": (created + timedelta(minutes=30)).isoformat() + "Z",
            "author": rng.choice(assignees),
            "note": "Ticket reviewed and assigned. Investigating the reported issue.",
        })
    if status == "resolved":
        updates.append({
            "timestamp": last_update.isoformat() + "Z",
            "author": rng.choice(assignees),
            "note": "Issue has been resolved. Please confirm the fix works on your end.",
        })
    if status == "waiting_on_user":
        updates.append({
            "timestamp": last_update.isoformat() + "Z",
            "author": rng.choice(assignees),
            "note": "Awaiting additional information from the requester to proceed.",
        })

    return {
        "ticket_id": ticket_id,
        "status": status,
        "priority": rng.choice(priorities),
        "category": rng.choice(categories),
        "assigned_to": rng.choice(assignees) if status != "open" else None,
        "created_at": created.isoformat() + "Z",
        "last_updated": last_update.isoformat() + "Z",
        "updates": updates,
        "message": f"Ticket {ticket_id} is currently {status.replace('_', ' ')}.",
    }


@tool
def reset_password(username: str, service: str = "email") -> dict:
    """Initiate a password reset for a user's account on a given service.

    Use this tool when a user is locked out of their account or needs a
    new password. A temporary password will be generated and the user
    will be required to change it on next login.

    Args:
        username: The username or employee ID of the account holder.
        service: The service to reset the password for - one of "email",
                 "vpn", "active_directory", "jira", "confluence", "slack",
                 "github", or "aws_console".

    Returns:
        A dict with the password reset outcome and next steps.
    """
    supported_services = {
        "email": "Corporate Email (Exchange Online)",
        "vpn": "VPN Gateway",
        "active_directory": "Active Directory",
        "jira": "Jira Project Management",
        "confluence": "Confluence Wiki",
        "slack": "Slack Workspace",
        "github": "GitHub Enterprise",
        "aws_console": "AWS Management Console",
    }

    if not username or len(username.strip()) < 2:
        return {
            "success": False,
            "error": "Invalid username. Please provide a valid username or employee ID.",
        }

    service_lower = service.lower().strip()
    if service_lower not in supported_services:
        return {
            "success": False,
            "error": f"Service '{service}' is not supported. "
                     f"Supported services: {', '.join(supported_services.keys())}.",
        }

    now = datetime.utcnow()
    temp_token = hashlib.sha256(
        f"{username}{service}{now.isoformat()}".encode()
    ).hexdigest()[:12].upper()

    return {
        "success": True,
        "username": username,
        "service": supported_services[service_lower],
        "reset_initiated_at": now.isoformat() + "Z",
        "temporary_password_info": {
            "delivery_method": "Sent to registered mobile via SMS",
            "token_reference": f"RST-{temp_token[:8]}",
            "expires_at": (now + timedelta(hours=1)).isoformat() + "Z",
            "must_change_on_login": True,
        },
        "instructions": [
            f"A temporary password has been sent to the mobile number on file for '{username}'.",
            f"Log in to {supported_services[service_lower]} with the temporary password.",
            "You will be prompted to create a new password on first login.",
            "The temporary password expires in 1 hour.",
            "If you do not receive the SMS within 5 minutes, contact IT directly.",
        ],
        "message": f"Password reset initiated for '{username}' on "
                   f"{supported_services[service_lower]}. "
                   f"A temporary password has been sent via SMS.",
    }


@tool
def check_system_status(system_name: str) -> dict:
    """Check the operational status of a company system or service.

    Use this tool to determine if a particular system is experiencing
    downtime, degraded performance, or is operating normally. Useful
    when users report issues that may be caused by system outages.

    Args:
        system_name: Name of the system to check (e.g. "email", "vpn",
                     "jira", "aws", "network", "erp", "salesforce").

    Returns:
        A dict with the system's current operational status and metrics.
    """
    systems = {
        "email": {
            "display_name": "Corporate Email (Exchange Online)",
            "status": "operational",
            "uptime_percent": 99.98,
            "response_time_ms": 45,
            "last_incident": "2026-10-15T08:30:00Z",
            "last_incident_summary": "Brief mail delivery delay (12 minutes). Resolved.",
        },
        "vpn": {
            "display_name": "VPN Gateway (Global)",
            "status": "operational",
            "uptime_percent": 99.95,
            "response_time_ms": 62,
            "last_incident": "2026-10-22T14:00:00Z",
            "last_incident_summary": "Increased latency on EU gateway. Resolved.",
        },
        "jira": {
            "display_name": "Jira Project Management",
            "status": "degraded",
            "uptime_percent": 99.80,
            "response_time_ms": 320,
            "last_incident": "2026-10-29T06:15:00Z",
            "last_incident_summary": "Slow page loads reported. Engineering investigating.",
        },
        "confluence": {
            "display_name": "Confluence Wiki",
            "status": "operational",
            "uptime_percent": 99.97,
            "response_time_ms": 78,
            "last_incident": "2026-10-01T10:00:00Z",
            "last_incident_summary": "Scheduled maintenance window. No unplanned downtime.",
        },
        "aws": {
            "display_name": "AWS Cloud Services",
            "status": "operational",
            "uptime_percent": 99.999,
            "response_time_ms": 12,
            "last_incident": "2026-09-20T03:00:00Z",
            "last_incident_summary": "us-east-1 API latency spike. Resolved in 8 minutes.",
        },
        "network": {
            "display_name": "Corporate Network & Wi-Fi",
            "status": "operational",
            "uptime_percent": 99.92,
            "response_time_ms": 8,
            "last_incident": "2026-10-25T16:45:00Z",
            "last_incident_summary": "Floor 3 access point reboot. 5-minute interruption.",
        },
        "erp": {
            "display_name": "SAP ERP System",
            "status": "operational",
            "uptime_percent": 99.90,
            "response_time_ms": 150,
            "last_incident": "2026-10-20T02:00:00Z",
            "last_incident_summary": "Scheduled nightly batch job overrun. No user impact.",
        },
        "salesforce": {
            "display_name": "Salesforce CRM",
            "status": "operational",
            "uptime_percent": 99.96,
            "response_time_ms": 95,
            "last_incident": "2026-10-10T11:30:00Z",
            "last_incident_summary": "Lightning component loading delay. Resolved.",
        },
        "slack": {
            "display_name": "Slack Workspace",
            "status": "operational",
            "uptime_percent": 99.99,
            "response_time_ms": 30,
            "last_incident": "2026-09-28T09:00:00Z",
            "last_incident_summary": "File upload slowness. Resolved by Slack.",
        },
        "github": {
            "display_name": "GitHub Enterprise",
            "status": "operational",
            "uptime_percent": 99.97,
            "response_time_ms": 55,
            "last_incident": "2026-10-18T07:20:00Z",
            "last_incident_summary": "Actions runner queue delay. Resolved.",
        },
    }

    key = system_name.lower().strip()
    if key in systems:
        info = systems[key]
        return {
            "system_name": info["display_name"],
            "status": info["status"],
            "uptime_percent": info["uptime_percent"],
            "response_time_ms": info["response_time_ms"],
            "last_incident": info["last_incident"],
            "last_incident_summary": info["last_incident_summary"],
            "checked_at": datetime.utcnow().isoformat() + "Z",
            "message": f"{info['display_name']} is currently {info['status']}. "
                       f"Uptime: {info['uptime_percent']}%.",
        }

    return {
        "system_name": system_name,
        "status": "unknown",
        "message": f"System '{system_name}' not found in monitoring. "
                   f"Known systems: {', '.join(systems.keys())}.",
        "known_systems": list(systems.keys()),
    }
