from datetime import datetime


VALID_LEVELS = {"low", "medium", "high"}


def calculate_priority(impact, urgency):
    """Calculate ticket priority using impact and urgency."""

    impact = impact.lower()
    urgency = urgency.lower()

    if impact not in VALID_LEVELS:
        raise ValueError("Impact must be low, medium, or high.")

    if urgency not in VALID_LEVELS:
        raise ValueError("Urgency must be low, medium, or high.")

    priority_matrix = {
        ("high", "high"): "Critical",
        ("high", "medium"): "High",
        ("high", "low"): "Medium",
        ("medium", "high"): "High",
        ("medium", "medium"): "Medium",
        ("medium", "low"): "Low",
        ("low", "high"): "Medium",
        ("low", "medium"): "Low",
        ("low", "low"): "Low",
    }

    return priority_matrix[(impact, urgency)]


def create_ticket(
    ticket_id,
    requester,
    department,
    title,
    description,
    impact,
    urgency,
):
    """Create and return a help desk ticket."""

    required_fields = {
        "Requester": requester,
        "Department": department,
        "Title": title,
        "Description": description,
    }

    for field_name, value in required_fields.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID cannot be empty.")

    priority = calculate_priority(impact, urgency)

    now = datetime.now().isoformat(timespec="seconds")

    ticket = {
        "ticket_id": ticket_id,
        "requester": requester.strip(),
        "department": department.strip(),
        "title": title.strip(),
        "description": description.strip(),
        "impact": impact.lower(),
        "urgency": urgency.lower(),
        "priority": priority,
        "assigned_to": None,
        "status": "Open",
        "created_at": now,
        "updated_at": now,
    }

    return ticket