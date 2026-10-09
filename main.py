from campusflow.tickets import create_ticket
from campusflow.workflow import (
    generate_ticket_id,
    assign_ticket,
    change_ticket_status,
    get_ticket_queue,
)
from campusflow.storage import (
    load_tickets,
    save_tickets,
    add_ticket,
    find_ticket,
)
from campusflow.reports import print_report


def display_menu():
    print("\n" + "=" * 45)
    print("          CAMPUSFLOW HELP DESK")
    print("=" * 45)
    print("1. Create ticket")
    print("2. View all tickets")
    print("3. View ticket details")
    print("4. Assign ticket")
    print("5. Change ticket status")
    print("6. View ticket queue")
    print("7. Generate reports")
    print("8. Exit")
    print("=" * 45)


def create_new_ticket(tickets):
    print("\n========== CREATE TICKET ==========")

    requester = input("Requester name: ").strip()
    department = input("Department: ").strip()
    title = input("Ticket title: ").strip()
    description = input("Description: ").strip()
    impact = input("Impact (low/medium/high): ").strip()
    urgency = input("Urgency (low/medium/high): ").strip()

    ticket_id = generate_ticket_id(tickets)

    try:
        ticket = create_ticket(
            ticket_id=ticket_id,
            requester=requester,
            department=department,
            title=title,
            description=description,
            impact=impact,
            urgency=urgency,
        )

        add_ticket(tickets, ticket)

        print("\nTicket created successfully!")
        print(f"Ticket ID: {ticket['ticket_id']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Status: {ticket['status']}")

    except ValueError as error:
        print(f"\nError: {error}")

    except OSError:
        print("\nError: Could not save the ticket.")


def view_all_tickets(tickets):
    print("\n========== ALL TICKETS ==========")

    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print(
            f"{ticket['ticket_id']} | "
            f"{ticket['title']} | "
            f"{ticket['priority']} | "
            f"{ticket['status']} | "
            f"Assigned to: {ticket['assigned_to'] or 'Unassigned'}"
        )


def view_ticket_details(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    print("\n========== TICKET DETAILS ==========")

    for key, value in ticket.items():
        print(f"{key.replace('_', ' ').title()}: {value}")


def assign_existing_ticket(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    staff_name = input("Enter staff member's name: ").strip()

    try:
        assign_ticket(ticket, staff_name)
        save_tickets(tickets)
        print(f"Ticket {ticket_id} assigned to {staff_name}.")

    except ValueError as error:
        print(f"Error: {error}")

    except OSError:
        print("Error: Could not save the assignment.")


def update_ticket_status(tickets):
    ticket_id = input("Enter ticket ID: ").strip()
    ticket = find_ticket(tickets, ticket_id)

    if ticket is None:
        print("Ticket not found.")
        return

    print("\nAvailable statuses:")
    print("1. Open")
    print("2. In Progress")
    print("3. Resolved")
    print("4. Closed")

    statuses = {
        "1": "Open",
        "2": "In Progress",
        "3": "Resolved",
        "4": "Closed",
    }

    choice = input("Choose a status: ").strip()
    new_status = statuses.get(choice)

    if new_status is None:
        print("Invalid choice.")
        return

    try:
        change_ticket_status(ticket, new_status)
        save_tickets(tickets)
        print(f"Ticket {ticket_id} status: {ticket['status']}")

    except ValueError as error:
        print(f"Error: {error}")

    except OSError:
        print("Error: Could not save the status change.")


def view_queue(tickets):
    queue = get_ticket_queue(tickets)

    print("\n========== ACTIVE TICKET QUEUE ==========")

    if not queue:
        print("No active tickets.")
        return

    for position, ticket in enumerate(queue, start=1):
        print(
            f"{position}. {ticket['ticket_id']} | "
            f"{ticket['priority']} | "
            f"{ticket['title']} | "
            f"{ticket['status']}"
        )


def main():
    try:
        tickets = load_tickets()
    except (OSError, ValueError) as error:
        print(f"Could not load tickets: {error}")
        return
    except Exception as error:
        print(f"Could not read ticket storage: {error}")
        return

    print("Welcome to CampusFlow!")

    while True:
        display_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            create_new_ticket(tickets)

        elif choice == "2":
            view_all_tickets(tickets)

        elif choice == "3":
            view_ticket_details(tickets)

        elif choice == "4":
            assign_existing_ticket(tickets)

        elif choice == "5":
            update_ticket_status(tickets)

        elif choice == "6":
            view_queue(tickets)

        elif choice == "7":
            print_report(tickets)

        elif choice == "8":
            print("Thank you for using CampusFlow. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()