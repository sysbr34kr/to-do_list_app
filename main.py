import task_options


def display_summary():
    total_tasks = len(task_options.tasks)
    active_tasks = sum(1 for task in task_options.tasks.values() if not task["completed"])
    completed_tasks = total_tasks - active_tasks
    deleted_tasks = task_options.deleted_count
    print(f"Total Tasks: {total_tasks} Active Tasks: {active_tasks} Completed Tasks: {completed_tasks} Deleted Tasks: {deleted_tasks}")


def display_menu():
    print("\nTo-Do List App")
    print("\nCurrent Tasks:")
    if task_options.tasks:
        for task_id, task in task_options.tasks.items():
            status = "Completed" if task["completed"] else "Pending"
            print(f"{task_id}: {task['description']} {[status]}")
    else:
        print("No tasks available.")
    display_summary()
    print("\nOptions:")
    print("1. Add a Task")
    print("2. Mark a Task as Completed")
    print("3. Delete a Task")
    print("4. Reset")
    print("5. Exit")


def main():
    task_options.load_tasks()
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        match choice:
            case "1":
                task_options.add_task()
            case "2":
                task_options.complete_task()
            case "3":
                task_options.delete_task()
            case "4":
                task_options.reset_tasks()
            case "5":
                task_options.save_tasks()
                print("\nSaving and Exiting...")
                break                
            case _:
                print("\nInvalid option, please try again.")


if __name__ == "__main__":
    main()