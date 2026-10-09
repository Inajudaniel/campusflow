import unittest

from campusflow.tickets import calculate_priority, create_ticket


class TestTicketPriority(unittest.TestCase):

    def test_high_impact_high_urgency_is_critical(self):
        result = calculate_priority("high", "high")
        self.assertEqual(result, "Critical")

    def test_medium_impact_medium_urgency_is_medium(self):
        result = calculate_priority("medium", "medium")
        self.assertEqual(result, "Medium")

    def test_low_impact_low_urgency_is_low(self):
        result = calculate_priority("low", "low")
        self.assertEqual(result, "Low")

    def test_invalid_impact_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("urgent", "high")

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_priority("high", "urgent")


class TestTicketCreation(unittest.TestCase):

    def test_ticket_is_created_successfully(self):
        ticket = create_ticket(
            ticket_id="CF-0001",
            requester="Daniel",
            department="Computer Science",
            title="Portal not opening",
            description="The student portal displays an error.",
            impact="high",
            urgency="high",
        )

        self.assertEqual(ticket["ticket_id"], "CF-0001")
        self.assertEqual(ticket["requester"], "Daniel")
        self.assertEqual(ticket["priority"], "Critical")
        self.assertEqual(ticket["status"], "Open")
        self.assertIsNone(ticket["assigned_to"])

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_ticket(
                ticket_id="CF-0002",
                requester="Daniel",
                department="Computer Science",
                title="",
                description="The student portal displays an error.",
                impact="high",
                urgency="high",
            )


if __name__ == "__main__":
    unittest.main()