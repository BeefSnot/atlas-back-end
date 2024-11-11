#!/usr/bin/python3
"""
This module fetches data from an API and exports it to a CSV file.
"""

import csv
import requests
import sys


def fetch_employee_todo_progress(employee_id):
    """
    Retrieves and displays the TODO list progress for a given employee.

    Args:
        employee_id (int): The ID of the employee.
    """
    user_url = (
        f"https://jsonplaceholder.typicode.com/users/{employee_id}"
        )
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print("Employee not found")
        return

    user_data = user_response.json()
    employee_name = user_response.json().get("name")
    username = user_data.get("username")

    todos_url = (
        f"https://jsonplaceholder.typicode.com/users/{employee_id}/todos"
        )
    todos_response = requests.get(todos_url)
    todos = todos_response.json()

    total_tasks = len(todos)
    done_tasks = [task for task in todos if task.get("completed")]
    number_of_done_tasks = len(done_tasks)

    print(
        f"Employee {employee_name} is done with tasks("
        f"{number_of_done_tasks}/{total_tasks}):"
        )

    for task in done_tasks:
        print(f"\t {task.get('title')}")

    csv_filename = f"{employee_id}.csv"
    with open(csv_filename, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for task in todos:
            csv_writer.writerow([
                employee_id,
                username,
                task["completed"],
                task["title"]
                ])
    print(f"Data exported to {csv_filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./script_name.py <employee_id>")
    else:
        try:
            employee_id = int(sys.argv[1])
            fetch_employee_todo_progress(employee_id)
        except ValueError:
            print("Employee ID must be an integer.")
