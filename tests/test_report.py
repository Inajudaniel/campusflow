import unittest

from campusflow.tickets import create_ticket
from campusflow.reports import generate_report


class TestReports(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            create_ticket(
                ticket_id="CF-0001",
                requester="Daniel",
                department="Computer Science",
                title="Portal problem",
                description="The portal is unavailable.",
                impact="high",
                urgency="high",
            ),
            create_ticket(
                ticket_id="CF-0002",
                requester="Grace",
                department="Library",
                title="Wi-Fi problem",
                description="The library Wi-Fi is slow.",
                impact="medium",
                urgency="high",
            ),
            create_ticket(
                ticket_id="CF-0003",
                requester="Peter",
                department="Administration",
                title="Software request",
                description="Software installation is needed.",
                impact="low",
                urgency="low",
            ),
        ]

        self.tickets[0]["assigned_to"] = "Daniel"
        self.tickets[0]["status"] = "In Progress"

        self.tickets[1]["assigned_to"] = "Daniel"
        self.tickets[1]["status"] = "Resolved"

    def test_total_ticket_count(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["total_tickets"], 3)

    def test_status_counts(self):
        report = generate_report(self.tickets)

        self.assertEqual(
            report["status_counts"]["In Progress"],
            1,
        )

        self.assertEqual(
            report["status_counts"]["Resolved"],
            1,
        )

        self.assertEqual(
            report["status_counts"]["Open"],
            1,
        )

    def test_priority_counts(self):
        report = generate_report(self.tickets)

        self.assertEqual(
            report["priority_counts"]["Critical"],
            1,
        )

        self.assertEqual(
            report["priority_counts"]["High"],
            1,
        )

        self.assertEqual(
            report["priority_counts"]["Low"],
            1,
        )

    def test_unassigned_ticket_count(self):
        report = generate_report(self.tickets)

        self.assertEqual(report["unassigned_tickets"], 1)

    def test_staff_workload(self):
        report = generate_report(self.tickets)

        self.assertEqual(
            report["staff_workloads"]["Daniel"],
            2,
        )

    def test_empty_report(self):
        report = generate_report([])

        self.assertEqual(report["total_tickets"], 0)
        self.assertEqual(report["unassigned_tickets"], 0)
        self.assertEqual(report["staff_workloads"], {})


if __name__ == "__main__":
    unittest.main()