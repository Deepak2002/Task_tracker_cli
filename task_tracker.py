# Importing required modules
import sys  # Provides access to command-line arguments and system-specific parameters
import json  # Used for reading and writing JSON data to a file
import os  # Used to interact with the operating system, like checking if a file exists
from datetime import datetime  # Used to get the current date and time

# File name where tasks are stored
TASKS_FILE = 'tasks.json'

# Function to load tasks from the JSON file
def load_tasks():
    # Check if the tasks file exists; if not, return an empty list
    if not os.path.exists(TASKS_FILE):
        return []

    # Open the tasks file in read mode and load the JSON data into a Python list
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

# Function to save tasks to the JSON file
def save_tasks(tasks):
    # Open the tasks file in write mode and save the tasks list as JSON
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)  # indent=4 for pretty-printing JSON

# Function to add a new task
def add_task(description):
    # Load existing tasks from the file
    tasks = load_tasks()
    # Generate a new task ID by getting the length of the tasks list and adding 1
    task_id = len(tasks) + 1
    # Create a new task dictionary with all necessary fields
    new_task = {
        'id': task_id,
        'description': description,
        'status': 'todo',  # Default status is 'todo'
        'createdAt': datetime.now().isoformat(),  # Current date and time in ISO format
        'updatedAt': datetime.now().isoformat()  # Same as created date for a new task
    }
    # Append the new task to the list of tasks
    tasks.append(new_task)
    # Save the updated tasks list back to the file
    save_tasks(tasks)
    # Print a confirmation message
    print(f"Task added successfully (ID: {task_id})")

# Function to update an existing task's description
def update_task(task_id, new_description):
    # Load existing tasks from the file
    tasks = load_tasks()
    # Find the task with the given ID
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    # If the task is not found, print a message and return
    if not task:
        print(f"Task with ID {task_id} not found.")
        return

    # Update the task's description and last updated timestamp
    task['description'] = new_description
    task['updatedAt'] = datetime.now().isoformat()
    # Save the updated tasks list back to the file
    save_tasks(tasks)
    # Print a confirmation message
    print(f"Task updated successfully (ID: {task_id})")

# Function to delete a task
def delete_task(task_id):
    # Load existing tasks from the file
    tasks = load_tasks()
    # Filter out the task with the given ID
    tasks = [task for task in tasks if task['id'] != task_id]
    # Save the updated tasks list back to the file
    save_tasks(tasks)
    # Print a confirmation message
    print(f"Task deleted successfully (ID: {task_id})")

# Function to mark a task with a specific status ('in-progress' or 'done')
def mark_task(task_id, status):
    # Load existing tasks from the file
    tasks = load_tasks()
    # Find the task with the given ID
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    # If the task is not found, print a message and return
    if not task:
        print(f"Task with ID {task_id} not found.")
        return

    # Update the task's status and last updated timestamp
    task['status'] = status
    task['updatedAt'] = datetime.now().isoformat()
    # Save the updated tasks list back to the file
    save_tasks(tasks)
    # Print a confirmation message
    print(f"Task marked as {status} (ID: {task_id})")

# Function to list tasks, optionally filtered by status
def list_tasks(status=None):
    # Load existing tasks from the file
    tasks = load_tasks()
    # If a status filter is provided, filter the tasks by status
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    
    # If no tasks are found, print a message and return
    if not tasks:
        print("No tasks found.")
        return

    # Loop through each task and print its details
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, "
              f"CreatedAt: {task['createdAt']}, UpdatedAt: {task['updatedAt']}")

# Main function to handle command-line input and execute the appropriate function
def main():
    # Check if the user has provided at least one command-line argument
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [<args>]")
        return

    # Get the command from the command-line arguments
    command = sys.argv[1]

    # Handle the 'add' command: add a new task
    if command == 'add' and len(sys.argv) == 3:
        add_task(sys.argv[2])
    # Handle the 'update' command: update an existing task
    elif command == 'update' and len(sys.argv) == 4:
        update_task(int(sys.argv[2]), sys.argv[3])
    # Handle the 'delete' command: delete a task
    elif command == 'delete' and len(sys.argv) == 3:
        delete_task(int(sys.argv[2]))
    # Handle the 'mark-in-progress' command: mark a task as in-progress
    elif command == 'mark-in-progress' and len(sys.argv) == 3:
        mark_task(int(sys.argv[2]), 'in-progress')
    # Handle the 'mark-done' command: mark a task as done
    elif command == 'mark-done' and len(sys.argv) == 3:
        mark_task(int(sys.argv[2]), 'done')
    # Handle the 'list' command: list tasks, optionally filtered by status
    elif command == 'list':
        if len(sys.argv) == 2:
            list_tasks()
        elif len(sys.argv) == 3:
            list_tasks(sys.argv[2])
    # Print an error message for invalid commands or arguments
    else:
        print("Invalid command or arguments.")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
