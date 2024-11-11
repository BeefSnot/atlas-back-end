#!/usr/bin/python3
"""
   This module gathers data from an API.

   This script fetches information about an employee's TODO list progress
   from a REST API and displays it in a specified format.

   Usage:
       python3 0-gather_data_from_an_API.py <employee_id>

   Example:
       python3 0-gather_data_from_an_API.py 2
"""

import sys
import requests


def get_employee_data(employee_id):
    """
    Retrieves employee data and TODO list progress from the API.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        tuple: A tuple containing the employee's name,
               a list of completed TODO titles, and the total number of tasks.
    """
    user_url = f"https://jsonplaceholder.typicode.com/users/{employee_id}"
    todos_url = f"https://jsonplaceholder.typicode.com/todos?userId={employee_id}"

    user_response = requests.get(user_url)
    todos_response = requests.get(todos_url)

    if user_response.status_code != 200 or todos_response.status_code != 200:
        return None, None, None

    user_data = user_response.json()
    todos_data = todos_response.json()

    completed_tasks = [
        todo.get("title") for todo in todos_data if todo.get("completed")
    ]
    total_tasks = len(todos_data)

    return user_data.get("name"), completed_tasks, total_tasks


def display_employee_progress(employee_id):
    """
    Displays the employee's TODO list progress in the specified format.

    Args:
        employee_id (int): The ID of the employee.
    """
    name, completed_tasks, total_tasks = get_employee_data(employee_id)

    if name is None or completed_tasks is None or total_tasks is None:
        print("Error fetching data.")
        return

    print(
        f"Employee {name} is done with tasks({len(completed_tasks)}/{total_tasks}):"
    )
    for task in completed_tasks:
        print(f"\t {task}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 0-gather_data_from_an_API.py <employee_id>")
        sys.exit(1)

    try:
        employee_id = int(sys.argv[1])
    except ValueError:
        print("Employee ID must be an integer.")
        sys.exit(1)

    display_employee_progress(employee_id)