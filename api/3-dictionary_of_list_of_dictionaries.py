#!/usr/bin/python3
"""
This module fetches data from an API and exports all
employees' to-do progress to a JSON file.
"""
import json
import requests
import sys


def fetch_employee_progress():
    """
    Fetches to-do progress of an employee by ID
    """
    # removed employee_id parameter

    # urls with data to be fetched
    base_url = "https://jsonplaceholder.typicode.com/"
    users_url = f"{base_url}users"
    todos_url = f"{base_url}todos"

    # fetch to-do list data
    todos_response = requests.get(todos_url)
    if todos_response.status_code != 200:
        print(f"To-Do List Fetch Fail")
        return
    todos_data = todos_response.json()

    # fetch user data
    users_response = requests.get(users_url)
    if users_response.status_code != 200:
        print(f"Name Fetch Fail")
        return
    users_data = users_response.json()

    # create dictionary of all employees' tasks by ID
    tasks_by_user = {}

    # map IDs to usernames for reference
    user_map = {user["id"]: user["username"] for user in users_data}

    # fetch task data for each employee
    for task in todos_data:
        user_id = task.get("userId")
        task_info = {
            "username": user_map.get(user_id),
            "task": task.get("title"),
            "completed": task.get("completed")
        }

        if user_id not in tasks_by_user:
            tasks_by_user[user_id] = []
        tasks_by_user[user_id].append(task_info)

    # export data to JSON file
    json_filename = "todo_all_employees.json"
    with open(json_filename, mode="w") as file:
        json.dump(tasks_by_user, file)


if __name__ == "__main__":
    fetch_employee_progress()