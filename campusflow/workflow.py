from datetime import datetime


VALID_STATUSES = {
    "Open",
    "In Progress",
    "Resolved",
    "Closed",
}

PRIORITY_ORDER = {
    "Critical": 0,
    "High": 1,
    "Medium": 2,
    "Low": 3,
}


def generate_ticket_id(tickets):
    """Generate a unique ticket ID."""

    highest_number = 0

    for ticket in tickets:
        ticket_id = ticket["ticket_id"]

        if ticket_id.startswith("CF-"):
            try:
                number = int(ticket_id[3:])
            except ValueError:
                continue

            highest_number = max(highest_number, number)

    return f"CF-{highest_number + 1:04d}"


def assign_ticket(ticket, staff_name):
    """Assign a ticket to a help desk staff member."""

    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name cannot be empty.")

    if ticket["status"] in {"Resolved", "Closed"}:
        raise ValueError("Cannot assign a resolved or closed ticket.")

    ticket["assigned_to"] = staff_name.strip()
    ticket["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return ticket


def change_ticket_status(ticket, new_status):
    """Change the status of a ticket."""

    if not isinstance(new_status, str):
        raise ValueError("Invalid ticket status.")

    normalized_status = new_status.strip().lower()

    status_lookup = {
        status.lower(): status for status in VALID_STATUSES
    }

    if normalized_status not in status_lookup:
        raise ValueError(
            "Status must be Open, In Progress, Resolved, or Closed."
        )

    new_status = status_lookup[normalized_status]
    current_status = ticket["status"]

    allowed_transitions = {
        "Open": {"In Progress", "Closed"},
        "In Progress": {"Open", "Resolved", "Closed"},
        "Resolved": {"In Progress", "Closed"},
        "Closed": set(),
    }

    if new_status == current_status:
        return ticket

    if new_status not in allowed_transitions[current_status]:
        raise ValueError(
            f"Cannot change status from {current_status} "
            f"to {new_status}."
        )

    ticket["status"] = new_status
    ticket["updated_at"] = datetime.now().isoformat(
        timespec="seconds"
    )

    return ticket


def get_ticket_queue(tickets):
    """Return active tickets in priority order."""

    active_tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] in {"Open", "In Progress"}
    ]

    return sorted(
        active_tickets,
        key=lambda ticket: (
            PRIORITY_ORDER.get(ticket["priority"], 99),
            ticket["created_at"],
            ticket["ticket_id"],
        ),
    )