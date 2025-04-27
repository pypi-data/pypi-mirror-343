import sys
from focus_cli.sprint import start_sprint, stop_sprint
from focus_cli.tasks import add_task, list_tasks, mark_task_done
from focus_cli.notes import add_note, list_notes
from focus_cli.goals import add_goal, list_goals
from focus_cli.quotes import random_dev_quote

def show_help():
    help_text = """
FocusCLI - Developer Productivity CLI

Commands:
    sprint start [--time MINUTES]    Start a coding sprint
    sprint stop                      Stop the current sprint
    tasks add "TASK_NAME"            Add a new task
    tasks list                       List all tasks
    tasks done TASK_ID               Mark a task as done
    notes add "NOTE_CONTENT"         Add a quick note
    notes list                       List all notes
    goals add "GOAL_NAME" [--type TYPE]  Add a new goal (type: daily, weekly, monthly)
    goals list                       List all goals
    quote dev                        Show a developer motivational quote
"""
    print(help_text)

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "sprint":
        if len(sys.argv) >= 3 and sys.argv[2] == "start":
            time = 25  # default 25 minutes
            if "--time" in sys.argv:
                idx = sys.argv.index("--time")
                if idx + 1 < len(sys.argv):
                    time = int(sys.argv[idx + 1])
            start_sprint(time)
        elif len(sys.argv) >= 3 and sys.argv[2] == "stop":
            stop_sprint()
        else:
            print("Invalid sprint command.")
            show_help()

    elif command == "tasks":
        if len(sys.argv) >= 3 and sys.argv[2] == "add":
            task_name = " ".join(sys.argv[3:])
            add_task(task_name)
        elif len(sys.argv) >= 3 and sys.argv[2] == "list":
            list_tasks()
        elif len(sys.argv) >= 4 and sys.argv[2] == "done":
            mark_task_done(int(sys.argv[3]))
        else:
            print("Invalid tasks command.")
            show_help()

    elif command == "notes":
        if len(sys.argv) >= 3 and sys.argv[2] == "add":
            note_content = " ".join(sys.argv[3:])
            add_note(note_content)
        elif len(sys.argv) >= 3 and sys.argv[2] == "list":
            list_notes()
        else:
            print("Invalid notes command.")
            show_help()

    elif command == "goals":
        if len(sys.argv) >= 3 and sys.argv[2] == "add":
            goal_name = " ".join(sys.argv[3:])
            goal_type = "daily"
            if "--type" in sys.argv:
                idx = sys.argv.index("--type")
                if idx + 1 < len(sys.argv):
                    goal_type = sys.argv[idx + 1]
            add_goal(goal_name, goal_type)
        elif len(sys.argv) >= 3 and sys.argv[2] == "list":
            list_goals()
        else:
            print("Invalid goals command.")
            show_help()

    elif command == "quote" and len(sys.argv) >= 3 and sys.argv[2] == "dev":
        random_dev_quote()

    else:
        print("Invalid command.")
        show_help()

if __name__ == "__main__":
    main()
