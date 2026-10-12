CampusFlow — AI-Native Campus Help Desk System
Project Overview

CampusFlow is a Python-based command-line help desk application designed to help campus IT support teams manage, prioritize, assign, and resolve technical support tickets efficiently.

The system allows users to report technical problems, automatically calculates ticket priority based on urgency and the number of affected users, tracks ticket progress, and generates reports to help support teams monitor their workload.
Key Features

    Ticket Creation: Create support tickets with unique IDs, titles, categories, urgency levels, and the number of affected users.
    Automatic Priority Calculation: Classify tickets as critical, high, medium, or low according to predefined rules.
    Ticket Management: View all tickets and inspect individual ticket details.
    Staff Assignment: Assign tickets to support staff.
    Status Tracking: Track tickets through the workflow: open, in progress, and resolved.
    Priority Queue: Display unresolved tickets in priority order.
    Reports: Generate summaries of ticket totals, statuses, and priority levels.
    Data Persistence: Save tickets to a JSON file and reload them when the application restarts.
    Input Validation: Reject invalid ticket information and inappropriate workflow transitions.
    Automated Testing: Use Python's built-in unittest framework to test application functionality.

Technologies Used

    Python 3
    JSON for data storage
    unittest for automated testing
    Git and GitHub for version control

Project Objective

The objective of CampusFlow is to demonstrate fundamental software engineering practices, including modular programming, input validation, business-rule implementation, data persistence, automated testing, and version control.

The project also emphasizes AI-native engineering practices, including using AI tools to assist with development, critically evaluating AI-generated suggestions, and documenting learning experiences.
Expected Outcome

CampusFlow aims to provide a simple help desk system that helps campus IT support teams organize technical issues, respond to urgent problems, and monitor the resolution of reported incidents.
Running the Application

    Ensure Python 3 is installed.

    Open a terminal in the project directory.

    Run the application: