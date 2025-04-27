import time
import json
from utils import load_json, save_json

# Path to sprints.json to track sprints
sprints_file = "data/sprints.json"

def start_sprint(minutes=25):
    """Starts a sprint by recording the start time and duration."""
    sprints = load_json(sprints_file)
    
    sprint_id = len(sprints) + 1  # Generate unique sprint ID
    start_time = time.time()  # Get current timestamp
    
    sprint = {
        "id": sprint_id,
        "start_time": start_time,
        "duration": minutes * 60,  # Convert minutes to seconds
        "status": "active"
    }
    
    sprints[sprint_id] = sprint
    save_json(sprints_file, sprints)
    
    print(f"Sprint {sprint_id} started! Time set for {minutes} minutes.")
    print(f"Focus! You're on the clock.")

def stop_sprint():
    """Stops the active sprint and calculates its duration."""
    sprints = load_json(sprints_file)
    
    active_sprints = [s for s in sprints.values() if s["status"] == "active"]
    
    if not active_sprints:
        print("No active sprint found.")
        return
    
    sprint = active_sprints[0]  # Only one active sprint
    sprint_end_time = time.time()
    sprint_duration = sprint_end_time - sprint["start_time"]
    
    sprint["status"] = "completed"
    sprint["end_time"] = sprint_end_time
    sprint["actual_duration"] = sprint_duration
    
    # Save updated sprint data
    save_json(sprints_file, sprints)
    
    print(f"Sprint {sprint['id']} completed!")
    print(f"Duration: {round(sprint_duration / 60, 2)} minutes.")

