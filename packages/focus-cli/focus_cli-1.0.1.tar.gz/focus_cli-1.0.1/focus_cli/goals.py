from utils import load_json, save_json
from datetime import datetime

# Path to goals.json to track goals
goals_file = "data/goals.json"

def add_goal(goal_name, description, target_date):
    """Adds a new goal to the list."""
    goals = load_json(goals_file)
    
    goal_id = len(goals) + 1  # Generate a unique goal ID
    goal = {
        "id": goal_id,
        "name": goal_name,
        "description": description,
        "target_date": target_date,
        "status": "in-progress",  # Default status for new goals
    }
    
    goals[goal_id] = goal
    save_json(goals_file, goals)
    
    print(f"Goal '{goal_name}' added! Goal ID: {goal_id}.")

def list_goals():
    """Lists all goals and their status."""
    goals = load_json(goals_file)
    
    if not goals:
        print("No goals available.")
        return
    
    print("Goals:")
    for goal in goals.values():
        print(f"ID: {goal['id']} - {goal['name']} (Status: {goal['status']}) - Target: {goal['target_date']}")

def mark_goal_completed(goal_id):
    """Marks a goal as completed by ID."""
    goals = load_json(goals_file)
    
    if goal_id not in goals:
        print(f"Goal with ID {goal_id} not found.")
        return
    
    goal = goals[goal_id]
    goal['status'] = 'completed'
    save_json(goals_file, goals)
    
    print(f"Goal '{goal['name']}' marked as completed.")
