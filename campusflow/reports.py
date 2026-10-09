from collections import Counter


def generate_report(tickets):
    """Generate statistics about help desk tickets."""

    status_counts = Counter(
        ticket["status"] for ticket in tickets
    )

    priority_counts = Counter(
        ticket["priority"] for ticket in tickets
    )

    assignment_counts = Counter(
        ticket["assigned_to"]
        for ticket in tickets
        if ticket["assigned_to"]
    )

    return {
        "total_tickets": len(tickets),
        "status_counts": {
            "Open": status_counts["Open"],
            "In Progress": status_counts["In Progress"],
            "Resolved": status_counts["Resolved"],
            "Closed": status_counts["Closed"],
        },
        "priority_counts": {
            "Critical": priority_counts["Critical"],
            "High": priority_counts["High"],
            "Medium": priority_counts["Medium"],
            "Low": priority_counts["Low"],
        },
        "unassigned_tickets": sum(
            1
            for ticket in tickets
            if not ticket["assigned_to"]
        ),
        "staff_workloads": dict(assignment_counts),
    }


def print_report(tickets):
    """Display the help desk report."""

    report = generate_report(tickets)

    print("\n" + "=" * 42)
    print("          CAMPUSFLOW REPORT")
    print("=" * 42)

    print(f"\nTotal tickets: {report['total_tickets']}")

    print("\nSTATUS BREAKDOWN")

    for status, count in report["status_counts"].items():
        print(f"{status:<15} {count}")

    print("\nPRIORITY BREAKDOWN")

    for priority, count in report["priority_counts"].items():
        print(f"{priority:<15} {count}")

    print("\nASSIGNMENT SUMMARY")
    print(f"Unassigned tickets: {report['unassigned_tickets']}")

    if report["staff_workloads"]:
        print("\nSTAFF WORKLOADS")

        for staff, count in sorted(
            report["staff_workloads"].items()
        ):
            print(f"{staff:<20} {count}")

    print("=" * 42)