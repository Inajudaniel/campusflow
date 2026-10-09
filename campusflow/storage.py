import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "tickets.json"


def save_tickets(tickets):
    """Save tickets to a JSON file."""

    temporary_file = DATA_FILE.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)

        temporary_file.replace(DATA_FILE)

    except OSError:
        if temporary_file.exists():
            temporary_file.unlink(missing_ok=True)

        raise


def load_tickets():
    """Load tickets from the JSON file."""

    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        tickets = json.load(file)

    if not isinstance(tickets, list):
        raise ValueError("Ticket storage must contain a JSON list.")

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise ValueError("Each ticket must be a JSON object.")

    return tickets


def add_ticket(tickets, ticket):
    """Add a ticket and save the updated collection."""

    if any(
        existing["ticket_id"] == ticket["ticket_id"]
        for existing in tickets
    ):
        raise ValueError(
            f"Ticket ID {ticket['ticket_id']} already exists."
        )

    tickets.append(ticket)

    try:
        save_tickets(tickets)
    except OSError:
        tickets.pop()
        raise

    return ticket


def find_ticket(tickets, ticket_id):
    """Find a ticket by its ID."""

    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return ticket

    return None