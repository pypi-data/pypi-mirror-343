from utils import load_json, save_json

# Path to tasks.json to track tasks
tasks_file = "data/tasks.json"

def add_task(task_name):
    """Adds a new task to the task list."""
    tasks = load_json(tasks_file)
    
    task_id = len(tasks) + 1  # Generate a unique task ID
    task = {
        "id": task_id,
        "name": task_name,
        "status": "pending"  # Default status for new tasks
    }
    
    tasks[task_id] = task
    save_json(tasks_file, tasks)
    
    print(f"Task '{task_name}' added! Task ID: {task_id}.")

def list_tasks():
    """Lists all tasks and their statuses."""
    tasks = load_json(tasks_file)
    
    if not tasks:
        print("No tasks available.")
        return
    
    print("Tasks:")
    for task in tasks.values():
        print(f"ID: {task['id']} - {task['name']} (Status: {task['status']})")

def mark_task_done(task_id):
    """Marks a task as done by its ID."""
    tasks = load_json(tasks_file)
    
    if task_id not in tasks:
        print(f"Task with ID {task_id} not found.")
        return
    
    task = tasks[task_id]
    task['status'] = 'done'
    save_json(tasks_file, tasks)
    
    print(f"Task '{task['name']}' marked as done.")
