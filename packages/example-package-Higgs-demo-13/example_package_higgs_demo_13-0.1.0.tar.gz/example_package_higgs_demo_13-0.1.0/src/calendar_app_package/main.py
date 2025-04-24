from .manager import TaskManager
from .calendar_api import calendar_api
from calendar_app_package.task import Task
from datetime import datetime

def parse_datetime(user_input):
    try:
        return datetime.strptime(user_input, "%m/%d/%Y %I:%M %p")
    except ValueError:
        raise ValueError("Invalid format. Please use MM/DD/YYYY HH:MM AM/PM (e.g., 04/29/2025 2:30 PM)")

def main():
    manager = TaskManager()
    calendar = calendar_api()

    print("Welcome to the Task Scheduler App")

    while True:
        print("\n====================")
        print("Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Exit")
        print("====================")

        choice = input("Choose an option (1, 2, or 3): ").strip()

        if choice == '1':
            print("\nEnter task details:")
            title = input("  • Title: ").strip()
            description = input("  • Description: ").strip()

            print("  • Start Time (MM/DD/YYYY HH:MM AM/PM)")
            start_raw = input("    > ").strip()

            print("  • End Time (MM/DD/YYYY HH:MM AM/PM)")
            end_raw = input("    > ").strip()

            try:
                start_dt = parse_datetime(start_raw)
                end_dt   = parse_datetime(end_raw)

                task = manager.add_task(title, description, start_dt.isoformat(), end_dt.isoformat())
                link = calendar.create_event(task)

                print("\nTask created and added to Google Calendar.")
                print(f"View event: {link}")
            except ValueError as ve:
                print(f"\n{ve}")
            except Exception as e:
                print(f"\nFailed to create task or calendar event: {e}")

        elif choice == '2':
            tasks = manager.list_tasks()
            if tasks:
                print("\nTask List:")
                for i, task in enumerate(tasks, start=1):
                    print(f"  {i}. {task}")
            else:
                print("\nNo tasks added yet.")

        elif choice == '3':
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# ignore covering the main because it will ALWAYS want to open a webpage I cant mock
if __name__ == '__main__':  # pragma: no cover
    main()