import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from campusflow.storage import (
    save_tickets,
    load_tickets,
    add_ticket,
    find_ticket,
)


class TestTicketStorage(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        self.data_file = Path(self.temp_dir.name) / "tickets.json"

        self.patcher = patch(
            "campusflow.storage.DATA_FILE",
            self.data_file,
        )

        self.patcher.start()

        self.ticket = {
            "ticket_id": "CF-0001",
            "requester": "Daniel",
            "department": "Computer Science",
            "title": "Portal not working",
            "description": "The portal displays an error.",
            "impact": "high",
            "urgency": "high",
            "priority": "Critical",
            "assigned_to": None,
            "status": "Open",
            "created_at": "2026-10-09T10:00:00",
            "updated_at": "2026-10-09T10:00:00",
        }

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_save_tickets(self):
        save_tickets([self.ticket])

        self.assertTrue(self.data_file.exists())

    def test_load_tickets(self):
        save_tickets([self.ticket])

        tickets = load_tickets()

        self.assertEqual(len(tickets), 1)
        self.assertEqual(
            tickets[0]["ticket_id"],
            "CF-0001",
        )

    def test_load_when_file_does_not_exist(self):
        tickets = load_tickets()

        self.assertEqual(tickets, [])

    def test_add_ticket(self):
        tickets = []

        add_ticket(tickets, self.ticket)

        self.assertEqual(len(tickets), 1)
        self.assertTrue(self.data_file.exists())

    def test_duplicate_ticket_id_is_rejected(self):
        tickets = [self.ticket]

        with self.assertRaises(ValueError):
            add_ticket(tickets, self.ticket)

    def test_find_ticket(self):
        tickets = [self.ticket]

        result = find_ticket(tickets, "CF-0001")

        self.assertEqual(
            result["requester"],
            "Daniel",
        )

    def test_find_missing_ticket(self):
        result = find_ticket([], "CF-9999")

        self.assertIsNone(result)

    def test_saved_data_is_valid_json(self):
        save_tickets([self.ticket])

        with self.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self.assertEqual(data[0]["priority"], "Critical")


if __name__ == "__main__":
    unittest.main()