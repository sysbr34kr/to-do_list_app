import tkinter as tk
from tkinter import messagebox
import task_options
import os


def update_summary(summary_label):
    total_tasks = task_options.task_id -1 if task_options.task_id > 1 else 0
    active_tasks = sum(1 for task in task_options.tasks.values() if not task["completed"])
    completed_tasks = total_tasks - active_tasks
    deleted_tasks = task_options.deleted_count
    summary_text = (
        f"Total Tasks: {total_tasks} | Active Tasks: {active_tasks} | "
        f"Completed Tasks: {completed_tasks} | Deleted Tasks: {deleted_tasks}"
    )
    summary_label.config(text = summary_text)


def open_add_task_window(parent, task_list, summary_label):
    def add_task_ui(summary_label):
        task_desc = task_entry.get().strip()
        if task_desc:
            task_options.tasks[str(task_options.task_id)] = {"description": task_desc, "completed": False}
            task_options.save_tasks()
            task_list.insert(tk.END, f"{task_options.task_id}: {task_desc} [Pending]")
            task_options.task_id += 1
            update_summary(summary_label)
            add_task_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty.")
    
    def cancel_add_task():
        add_task_window.destroy()

    add_task_window = tk.Toplevel(parent)
    add_task_window.title("Add Task")
    add_task_window.geometry("400x200")
    add_task_window.grab_set()

    task_label = tk.Label(add_task_window, text = "Task Description:")
    task_label.pack(pady = 10)
    task_entry = tk.Entry(add_task_window, width = 40)
    task_entry.pack(pady = 10)

    button_frame = tk.Frame(add_task_window)
    button_frame.pack(pady = 20)

    add_button = tk.Button(button_frame, text = "Add", width = 10, command = lambda: add_task_ui(summary_label))
    add_button.pack(side = tk.LEFT, padx = 10)

    cancel_button = tk.Button(button_frame, text = "Cancel", width = 10, command = cancel_add_task)
    cancel_button.pack(side = tk.LEFT, padx = 10)


def complete_task_ui(task_list, summary_label):
    selected = task_list.curselection()
    if selected:
        index = selected[0]
        task_info = task_list.get(index)
        try:
            t_id = int(task_info.split(":")[0])
        except ValueError:
            messagebox.showerror("Task Error", "Unable to parse task ID.")
            return
        if str(t_id) in task_options.tasks:
            if not task_options.tasks[str(t_id)]["completed"]:
                task_options.tasks[str(t_id)]["completed"] = True
                task_options.save_tasks()
                task_desc = task_options.tasks[str(t_id)]["description"]
                task_list.delete(index)
                task_list.insert(index, f"{t_id}: {task_desc} [Completed]")
                update_summary(summary_label)
            else:
                messagebox.showinfo("Task Completed", "Task is already marked as completed.")
        else:
            messagebox.showerror("Task Error", "Task ID not found.")
    else:
        messagebox.showwarning("Selection Error", "No task selected.")


def delete_task_ui(task_list, summary_label):
    selected = task_list.curselection()
    if selected:
        index = selected[0]
        task_info = task_list.get(index)
        print(f"DEBUG: Selected Task Info: {task_info}")
        try:
            t_id = int(task_info.split(":")[0])
            print(f"DEBUG: Extracted Task ID: {t_id}")
        except ValueError:
            messagebox.showerror("Task Error", "Unable to parse task ID.")
            return
        
        if str(t_id) in task_options.tasks:
            del task_options.tasks[str(t_id)]
            task_options.deleted_count += 1
            task_options.save_tasks()
            task_list.delete(index)
            update_summary(summary_label)
        else:
            print(f"DEBUG: Task ID {t_id} not found in tasks: {task_options.tasks.keys()}")
            messagebox.showerror("Task Error", "Task ID not found.")
    else:
        messagebox.showwarning("Selection Error", "No task selected.")


def reset_tasks_ui(task_list, summary_label):
    confirm = messagebox.askyesno("Reset Tasks", "This will delete all tasks and reset the archive. Are you sure?")
    if confirm:
        task_options.tasks.clear()
        task_options.task_id = 1
        task_options.deleted_count = 0
        if task_options.file_path and os.path.exists(task_options.file_path):
            os.remove(task_options.file_path)
        task_options.save_tasks()
        task_list.delete(0, tk.END)
        update_summary(summary_label)
        messagebox.showinfo("Reset", "All tasks have been reset.")


def main():
    task_options.load_tasks()
    root = tk.Tk()
    root.title("To-Do List")
    
    summary_label = tk.Label(root, text = "", font = ("Arial", 12), anchor = "w", bg = "Lightgrey", relief = "sunken", padx = 5)
    summary_label.pack(side = tk.TOP, fill = tk.X)
    update_summary(summary_label)

    task_frame = tk.Frame(root)
    task_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = True, pady = 10)
    
    task_list = tk.Listbox(root, width = 80, height = 15)
    task_list.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

    for t_id, task in task_options.tasks.items():
        status = "Completed" if task["completed"] else "Pending"
        task_list.insert(tk.END, f"{int(t_id)}: {task['description']} [{status}]")

    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side = tk.BOTTOM, fill = tk.X, pady = 10)

    button_frame = tk.Frame(bottom_frame)
    button_frame.pack(side = tk.LEFT, padx = 10)

    add_button = tk.Button(button_frame, text = "Add Task", width = 15, command = lambda: open_add_task_window(root, task_list, summary_label))
    add_button.pack(side = tk.LEFT, padx = 5)

    mark_button = tk.Button(button_frame, text = "Mark as Completed", width = 15, command = lambda: complete_task_ui(task_list, summary_label))
    mark_button.pack(side = tk.LEFT, padx = 5)
    
    delete_button = tk.Button(button_frame, text = "Delete Task", width = 15, command = lambda: delete_task_ui(task_list, summary_label))
    delete_button.pack(side = tk.LEFT, padx = 5)

    reset_button = tk.Button(button_frame, text = "Reset", width = 15, command = lambda: reset_tasks_ui(task_list, summary_label))
    reset_button.pack(side = tk.LEFT, padx = 5)

    root.geometry("800x500")
    root.mainloop()


if __name__ == "__main__":
    main()