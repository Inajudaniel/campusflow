import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import (
    generate_ticket_id,
    assign_ticket,
    change_ticket_status,
    get_ticket_queue,
)


class TestTicketWorkflow(unittest.TestCase):

    def setUp(self):
        self.ticket = create_ticket(
            ticket_id="CF-0001",
            requester="Daniel",
            department="Computer Science",
            title="Student portal problem",
            description="The portal is not opening.",
            impact="high",
            urgency="high",
        )

    def test_generate_ticket_id(self):
        tickets = [self.ticket]

        result = generate_ticket_id(tickets)

        self.assertEqual(result, "CF-0002")

    def test_generate_first_ticket_id(self):
        result = generate_ticket_id([])

        self.assertEqual(result, "CF-0001")

    def test_assign_ticket(self):
        assign_ticket(self.ticket, "Daniel")

        self.assertEqual(
            self.ticket["assigned_to"],
            "Daniel",
        )

    def test_empty_staff_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket(self.ticket, "")

    def test_change_ticket_status(self):
        change_ticket_status(self.ticket, "In Progress")

        self.assertEqual(
            self.ticket["status"],
            "In Progress",
        )

    def test_invalid_status_is_rejected(self):
        with self.assertRaises(ValueError):
            change_ticket_status(self.ticket, "Pending")

    def test_closed_ticket_cannot_be_reopened(self):
        change_ticket_status(self.ticket, "Closed")

        with self.assertRaises(ValueError):
            change_ticket_status(self.ticket, "Open")

    def test_queue_orders_tickets_by_priority(self):
        low_ticket = create_ticket(
            ticket_id="CF-0002",
            requester="Student A",
            department="Library",
            title="Library software request",
            description="I need software installed.",
            impact="low",
            urgency="low",
        )

        tickets = [low_ticket, self.ticket]

        queue = get_ticket_queue(tickets)

        self.assertEqual(
            queue[0]["ticket_id"],
            "CF-0001",
        )

        self.assertEqual(
            queue[1]["ticket_id"],
            "CF-0002",
        )

    def test_resolved_tickets_are_excluded_from_queue(self):
        change_ticket_status(self.ticket, "In Progress")
        change_ticket_status(self.ticket, "Resolved")

        queue = get_ticket_queue([self.ticket])

        self.assertEqual(queue, [])


if __name__ == "__main__":
    unittest.main()