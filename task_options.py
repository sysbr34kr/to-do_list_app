import json
import os

tasks = {}
task_id = 1
deleted_count = 0
file_path = "tasks.json"


def save_tasks():
    global tasks, task_id, deleted_count
    data = {
        "tasks": tasks,
        "task_id": task_id,
        "deleted_count": deleted_count,
    }
    with open(file_path, "w") as file:
        json.dump(data, file, indent = 4)
    print("\nTasks saved.")


def load_tasks():
    global tasks, task_id, deleted_count
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            tasks = data.get("tasks", {})
            task_id = data.get("task_id", 1)
            deleted_count = data.get("deleted_count", 0)
    except FileNotFoundError:
        print("\nFile not found. Creating new file.")
    except json.JSONDecodeError:
        print("\nError loading file. Creating new file.")


def reset_tasks():
    global tasks, task_id, deleted_count
    confirm = input("\nThis will delete all tasks and reset the archive. Are you sure? (y/N)").strip().lower()
    if confirm == "y":
        tasks.clear()
        task_id = 1
        deleted_count = 0
        if os.path.exists(file_path):
            os.remove(file_path)
        save_tasks()
        print("\nFile deleted.")
    else:
        print("\nReset canceled.")


def add_task():
    global task_id
    description = input("\nEnter task description: ").strip()
    if description:
        print(f"\nTask description: {description}")
        confirm = input("Add this task? (Y/n)").strip().lower()
        if confirm in ("y", ""):
            tasks[task_id] = {"description": description, "completed": False}
            print(f"\nTask added with ID: {task_id}")
            save_tasks()
            task_id += 1
        else: 
            print("\nTask creation canceled.")
    else:
        print("\nDescription cannot be empty.")


def complete_task():
    if not tasks:
        print("\nNo tasks to be completed.")
        return
    else:
        print("\n")
        for t_id, task in tasks.items():
            status = "Completed" if task["completed"] else "Pending"
            print(f"{t_id}: {task['description']} {[status]}")
    
    try:
        t_id = int(input("\nEnter task ID to mark as completed: ").strip())
        if t_id in tasks:
            if tasks[t_id]["completed"]:
                print(f"\nTask {t_id} is already completed")
            else:
                print(f"\n{t_id}: {tasks[t_id]['description']} [Pending]")
                confirm = input("\nMark this task as completed? (Y/n)").strip().lower()
                if confirm in ("y", ""):
                    tasks[t_id]["completed"] = True
                    save_tasks()
                    print(f"\nTask {t_id} completed!")
                else: 
                    print("\nTask completion canceled.")
        else:
            print("\nInvalid task ID.")
    except ValueError:
        print("\nPlease enter a valid numeric task ID")


def delete_task():
    global deleted_count
    if not tasks:
        print("\nNo tasks to delete.")
        return
    else:
        print("\n")
        for t_id, task in tasks.items():
            status = "Completed" if task["completed"] else "Pending"
            print(f"{t_id}: {task['description']} {[status]}")
    
    try:
        t_id = int(input("\nEnter task ID for delete: ").strip())
        if t_id in tasks:
            status = "Completed" if tasks[t_id]["completed"] else "Pending"
            print(f"\n{t_id}: {tasks[t_id]['description']} {[status]}")
            confirm = input("\nAre you sure you want to delete this task? (Y/n)").strip().lower()
            if confirm in ("y", ""):
                del tasks[t_id]
                deleted_count += 1
                save_tasks()
                print(f"\nTask {t_id} deleted.")
            else:
                print("Task deletion canceled.")
        else:
            print("\nInvalid task ID.")
    except ValueError:
        print("\nPlease enter a valid numeric task ID")