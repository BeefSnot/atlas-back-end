#!/usr/bin/python3
"""
This module fetches data from an API and exports it to a JSON file.
"""
import json
import requests
import sys


def fetch_employee_progress(employee_id):
    """
    Fetches to-do progress of an employee by ID
    """
    # check if employee_id is an integer
    if not isinstance(employee_id, int):
        raise TypeError("employee_id must be an integer.")

    # urls with data to be fetched
    base_url = "https://jsonplaceholder.typicode.com/"
    user_url = f"{base_url}users/{employee_id}"
    todo_url = f"{base_url}todos?userId={employee_id}"

    # fetch to-do list data
    todo_response = requests.get(todo_url)
    if todo_response.status_code != 200:
        print(f"To-Do List Fetch Fail: {employee_id}")
        return
    todo_data = todo_response.json()

    # fetch user data
    user_response = requests.get(user_url)
    if user_response.status_code != 200:
        print(f"Name Fetch Fail: {employee_id}")
        return
    user_data = user_response.json()

    # fetch employee name
    employee_name = user_data.get("username")

    # format data to be exported to JSON
    tasks_list = []
    for task in todo_data:
        task_info = {
            "task": task.get("title"),
            "completed": task.get("completed"),
            "username": employee_name
        }
        tasks_list.append(task_info)

    json_data = {str(employee_id): tasks_list}

    # export data to JSON file
    json_filename = f"{employee_id}.json"
    with open(json_filename, mode="w") as file:
        json.dump(json_data, file, separators=(",", ":"))
    return json_data


if __name__ == "__main__":
    fetch_employee_progress(int(sys.argv[1]))