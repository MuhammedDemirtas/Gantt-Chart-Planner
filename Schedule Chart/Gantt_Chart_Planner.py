import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
from tkcalendar import DateEntry
import json

schedule = []

PROJECTS_FILE = "projects.json"

def load_project(file_name):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            for item in data:
                item["Start"] = datetime.strptime(item["Start"], "%Y-%m-%d")
                item["End"] = datetime.strptime(item["End"], "%Y-%m-%d")
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "The data file is corrupted.")
        return []

def save_project(file_name):
    with open(file_name, "w") as file:
        data = [
            {
                "Task": task["Task"],
                "Person": task["Person"],
                "Start": task["Start"].strftime("%Y-%m-%d"),
                "End": task["End"].strftime("%Y-%m-%d"),
                "Color": task["Color"],
                "Progress": task.get("Progress", 0),
                "Priority": task.get("Priority", "Mid")
            }
            for task in schedule
        ]
        json.dump(data, file)

def list_projects():
    try:
        with open(PROJECTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def add_project(project_name):
    projects = list_projects()
    if project_name not in projects:
        projects.append(project_name)
        with open(PROJECTS_FILE, "w") as file:
            json.dump(projects, file)

def add_task(task_name, person, start_date, end_date, color, progress, priority):
    global schedule
    schedule.append({
        "Task": task_name,
        "Person": person,
        "Start": datetime.strptime(start_date, "%Y-%m-%d"),
        "End": datetime.strptime(end_date, "%Y-%m-%d"),
        "Color": color,
        "Progress": progress,
        "Priority": priority
    })

def delete_task(task_name):
    global schedule
    schedule = [task for task in schedule if task["Task"] != task_name]

def edit_task(old_task_name, new_task_data):
    global schedule
    for task in schedule:
        if task["Task"] == old_task_name:
            task.update(new_task_data)

def check_deadlines():
    today = datetime.now()
    warnings = []
    for task in schedule:
        task_end_datetime = datetime.combine(task["End"], datetime.min.time())
        remaining_days = (task_end_datetime - today).days
        if 0 <= remaining_days <= 10:
            warnings.append(f"The deadline for task {task['Task']} is approaching ({remaining_days} days left).")

    if warnings:
        messagebox.showwarning("Upcoming Deadlines", "\n".join(warnings))
    else:
        messagebox.showinfo("Information", "No upcoming deadlines.")

def create_gantt_chart():
    if not schedule:
        messagebox.showwarning("Warning", "Please add a task before creating a Gantt chart.")
        return

    df = pd.DataFrame(schedule)
    df = df.sort_values(by="Start")

    fig, ax = plt.subplots(figsize=(10, len(schedule) * 0.4))  # Adjusted height for thinner bars

    annotation = None

    for i, task in enumerate(df.itertuples()):
        start = task.Start
        end = task.End
        color = task.Color
        progress = task.Progress / 100

        bar1 = ax.barh(i, (end - start).days * progress, left=start, color="green", height=0.4)
        bar2 = ax.barh(i, (end - start).days * (1 - progress), left=start + (end - start) * progress, color=color, alpha=0.5, height=0.4)

        # Adding hover text for progress percentage
        for bar in bar1:
            bar.set_picker(True)
            bar.set_gid(f"Progress: {task.Progress}%")

        for bar in bar2:
            bar.set_picker(True)
            bar.set_gid(f"Remaining: {100 - task.Progress}%")

        ax.text(start, i, f"{task.Task} ({task.Person})", va="center", ha="left", fontsize=9)

    def on_hover(event):
        nonlocal annotation
        if annotation:
            annotation.remove()
            annotation = None
            fig.canvas.draw_idle()

        if event.inaxes == ax:
            for bar in ax.patches:
                if bar.contains(event)[0]:
                    gid = bar.get_gid()
                    annotation = ax.annotate(
                        gid,
                        xy=(event.xdata, event.ydata),
                        xytext=(15, 15),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w", ec="k"),
                        arrowprops=dict(arrowstyle="->")
                    )
                    fig.canvas.draw_idle()
                    break

    fig.canvas.mpl_connect("motion_notify_event", on_hover)

    ax.set_yticks(range(len(schedule)))
    ax.set_yticklabels(df["Task"])
    ax.xaxis_date()
    ax.set_xlabel("Date")
    ax.set_title("Gantt Chart")

    plt.subplots_adjust(top=0.9, bottom=0.2)

    plt.tight_layout()
    plt.show()

    save_pdf = messagebox.askyesno("Save as PDF", "Do you want to save the Gantt chart as a PDF?")
    if save_pdf:
        file_name = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Gantt Chart"
        )
        if file_name:
            fig.savefig(file_name, format="pdf")
            messagebox.showinfo("Success", f"Gantt chart saved as {file_name}.")

def main_menu():

    def destroy_window():
        root.destroy()

    def open_existing_project():
        project_name = project_selection.get()
        if not project_name:
            messagebox.showerror("Error", "Please select a project.")
            return

        global schedule
        schedule = load_project(f"{project_name}.json")
        root.destroy()
        main_gui(project_name)

    def create_new_project():
        project_name = new_project_name.get()
        if not project_name:
            messagebox.showerror("Error", "Project name cannot be empty.")
            return

        global schedule
        schedule = []
        save_project(f"{project_name}.json")
        add_project(project_name)
        root.destroy()
        main_gui(project_name)

    root = tk.Tk()
    root.title("Project Schedule Planner")

    root.attributes("-fullscreen", True)

    window_width = 1920
    window_height = 1080
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

    frame = ttk.Frame(root)
    frame.pack(expand=True, padx=100, pady=200, fill="both")

    separator = ttk.Separator(frame, orient="horizontal")
    separator.pack(fill="x", pady=10, padx=400)

    ttk.Label(frame, text="Existing Projects", font=("Arial", 14)).pack(pady=15)
    project_selection = ttk.Combobox(frame, values=list_projects(), state="readonly", width=30)
    project_selection.pack(pady=15)

    ttk.Button(frame, text="Open Project", command=open_existing_project, width=20).pack(pady=15)

    separator = ttk.Separator(frame, orient="horizontal")
    separator.pack(fill="x", pady=10, padx=400)

    ttk.Label(frame, text="New Project Name", font=("Arial", 14)).pack(pady=15)
    new_project_name = ttk.Entry(frame, width=30)
    new_project_name.pack(pady=15)

    ttk.Button(frame, text="Create New Project", command=create_new_project, width=20).pack(pady=15)

    ttk.Button(frame, text="Exit", command=destroy_window, width=20).pack(pady=15)

    separator = ttk.Separator(frame, orient="horizontal")
    separator.pack(fill="x", pady=10, padx=400)

    root.mainloop()

def main_gui(project_name):
    def add_task_gui():
        task_name = task_entry.get()
        person = person_entry.get()
        start_date = start_entry.get_date().strftime("%Y-%m-%d")
        end_date = end_entry.get_date().strftime("%Y-%m-%d")
        color = color_var.get()
        progress = int(progress_entry.get())
        priority = priority_var.get()

        if not task_name or not person:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        add_task(task_name, person, start_date, end_date, color, progress, priority)
        task_entry.delete(0, tk.END)
        person_entry.delete(0, tk.END)
        progress_entry.delete(0, tk.END)
        update_task_list()

    def choose_color():
        color_code = colorchooser.askcolor(title="Choose Color")
        if color_code:
            color_var.set(color_code[1])

    def save_current_project():
        save_project(f"{project_name}.json")
        task_entry.delete(0, tk.END)
        person_entry.delete(0, tk.END)
        progress_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"{project_name} has been successfully saved.")

    def delete_task_gui():
        selected_task = task_listbox.get(task_listbox.curselection())
        if not selected_task:
            messagebox.showerror("Error", "Please select a task.")
            return

        task_name = selected_task.split(" (")[0]
        delete_task(task_name)
        update_task_list()

    def edit_task_gui():
        try:
            selected_task = task_listbox.get(task_listbox.curselection())
            task_name = selected_task.split(" (")[0]

            for task in schedule:
                if task["Task"] == task_name:
                    task_entry.delete(0, tk.END)
                    person_entry.delete(0, tk.END)
                    progress_entry.delete(0, tk.END)

                    task_entry.insert(0, task["Task"])
                    person_entry.insert(0, task["Person"])
                    start_entry.set_date(task["Start"])
                    end_entry.set_date(task["End"])
                    color_var.set(task["Color"])
                    progress_entry.insert(0, task["Progress"])
                    priority_var.set(task["Priority"])

                    def save_edits():
                        task["Task"] = task_entry.get()
                        task["Person"] = person_entry.get()
                        task["Start"] = start_entry.get_date()
                        task["End"] = end_entry.get_date()
                        task["Color"] = color_var.get()
                        task["Progress"] = int(progress_entry.get())
                        task["Priority"] = priority_var.get()

                        update_task_list()
                        save_current_project()
                        task_entry.delete(0, tk.END)
                        person_entry.delete(0, tk.END)
                        progress_entry.delete(0, tk.END)
                        messagebox.showinfo("Success", "Task successfully updated.")

                        save_edits()

        except tk.TclError:
            messagebox.showerror("Error", "Please select a task.")


    def update_task():
        selected_index = task_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a task.")
            return

        selected_task = task_listbox.get(selected_index)
        task_name = selected_task.split(" (")[0]

        try:
            new_task_data = {
                "Task": task_entry.get(),
                "Person": person_entry.get(),
                "Start": datetime.combine(start_entry.get_date(), datetime.min.time()),
                "End": datetime.combine(end_entry.get_date(), datetime.min.time()),
                "Color": color_var.get(),
                "Progress": int(progress_entry.get()),
                "Priority": priority_var.get()
            }

            edit_task(task_name, new_task_data)
            task_entry.delete(0, tk.END)
            person_entry.delete(0, tk.END)
            progress_entry.delete(0, tk.END)
            update_task_list()
            messagebox.showinfo("Success", "Task successfully updated.")
        except ValueError:
            messagebox.showerror("Error", "Invalid completion percentage. Please enter a number.")


    def update_task_list():
        task_listbox.delete(0, tk.END)
        for task in schedule:
            task_listbox.insert(
                tk.END,
                f"{task['Task']} ({task['Person']}) - {task['Priority']} - ({task['Start']}) - ({task['End']})"
            )

    def go_to_back():
        root.destroy()
        main_menu()

    def destroy_window():
        root.destroy()

    root = tk.Tk()
    root.title(f"Project {project_name}")

    root.attributes("-fullscreen", True)

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew", padx=500, pady=100)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=2)

    ttk.Label(frame, text="Task Name").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
    task_entry = ttk.Entry(frame, width=30)
    task_entry.grid(row=0, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="Person Responsible").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    person_entry = ttk.Entry(frame, width=30)
    person_entry.grid(row=1, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="Start Date").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    start_entry = DateEntry(frame, date_pattern="yyyy-mm-dd")
    start_entry.grid(row=2, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="End Date").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    end_entry = DateEntry(frame, date_pattern="yyyy-mm-dd")
    end_entry.grid(row=3, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="Color").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
    color_var = tk.StringVar(value="#FFFFFF")
    color_button = ttk.Button(frame, text="Choose Color", command=choose_color)
    color_button.grid(row=4, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="Completion (%)").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
    progress_entry = ttk.Entry(frame, width=30)
    progress_entry.grid(row=5, column=1, pady=5, sticky="ew")

    ttk.Label(frame, text="Priority").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
    priority_var = tk.StringVar(value="Medium")
    priority_menu = ttk.Combobox(frame, textvariable=priority_var, values=["Low", "Medium", "High"])
    priority_menu.grid(row=6, column=1, pady=5, sticky="ew")

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

    ttk.Button(button_frame, text="Add Task", command=add_task_gui).grid(row=0, column=0, padx=3, pady=5, sticky="ew")
    ttk.Button(button_frame, text="Update Task", command=update_task).grid(row=0, column=1, padx=3, pady=5, sticky="ew")
    ttk.Button(frame, text="Edit Task", command=edit_task_gui).grid(row=7, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(frame, text="Task List").grid(row=8, column=0, sticky=tk.W, padx=10, pady=5)
    task_listbox = tk.Listbox(frame, height=10, width=30)
    task_listbox.grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

    ttk.Button(frame, text="Delete Task", command=delete_task_gui).grid(row=8, column=1, padx=10, pady=5, sticky="ew")

    ttk.Button(frame, text="Back", command=go_to_back).grid(row=10, column=0, columnspan=2, pady=5, sticky="ew")

    ttk.Button(frame, text="Create Gantt Chart", command=create_gantt_chart).grid(row=11, column=0, pady=5, sticky="ew")
    ttk.Button(frame, text="Check Upcoming Deadlines", command=check_deadlines).grid(row=11, column=1, pady=5, sticky="ew")
    ttk.Button(frame, text="Save Gantt", command=save_current_project).grid(row=12, column=0, columnspan=2, pady=10, sticky="ew")

    exit_button = ttk.Button(frame, text="Exit", command=destroy_window)
    exit_button.grid(row=13, column=0, columnspan=2, pady=10, sticky="ew")

    update_task_list()
    root.mainloop()

if __name__ == "__main__":
    main_menu()

