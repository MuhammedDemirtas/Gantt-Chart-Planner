# Gantt Schedule Chart Planner

---

This Python-based Gantt Chart Planner allows you to visualize and manage project schedules. It enables you to create tasks, define durations, set dependencies, and track progress in a Gantt chart format.

---

## Features

- **Task Management**:
  - Create, edit, and delete tasks with ease.
  - Assign tasks to individuals and set task priorities (Low, Medium, High).
  - Track task progress with a percentage completion indicator.
- **Date Management**:
  - Define start and end dates for tasks.
  - Visualize tasks and their durations in a Gantt chart.
  - Highlight tasks with approaching deadlines (10 days or less).
- **Visual Customization**:
  - Assign custom colors to tasks for better visualization.
  - View progress and remaining work visually on the Gantt chart.
  - Interactive hover functionality for detailed task progress.
- **Project Management**:
  - Save and load projects to continue work seamlessly.
  - List and manage multiple projects.
  - Create new projects with an intuitive GUI.
- **Export Options**:
  - Export Gantt charts as PDF files for easy sharing.

---

## Installation

```bash
git clone https://github.com/MuhammedDemirtas/Gantt-Schedule-Chart-Planner.git
cd Gantt-Schedule-Chart-Planner
pip install -r requirements.txt
```

---

## Running the Application

After installing the dependencies, you can run the application using:

```bash
python Gantt_Chart_Planner.py
```

This will launch the Gantt Chart Planner, allowing you to define and manage your project tasks through an interactive graphical interface.

---

## Code Overview

### `Gantt_chart_planner.py`
- The main entry point of the application. It loads the interface and controls the overall project flow.
- Handles the creation and visualization of the Gantt chart.
- Manages tasks, including their properties (e.g., start date, end date, progress, priority).
- Provides utility functions for saving and loading projects.

### `projects.json`
- A file that holds the names of different projects, acting as a reference for all saved projects.
- Ensures smooth navigation and tracking of project details within the Gantt Chart Planner.

---

## New Features and Enhancements

1. **Interactive Gantt Chart**:
   - Hover over tasks in the chart to view progress and remaining work details.
   - Enhanced visual representation with split bars for completed and remaining work.

2. **Deadline Management**:
   - Receive warnings for tasks with deadlines approaching within 10 days.
   - Highlight deadlines in the interface for better project tracking.

3. **Task Customization**:
   - Assign custom colors to tasks.
   - View and manage task priorities directly in the interface.

4. **Improved GUI**:
   - Intuitive menus for creating, editing, and managing tasks.
   - Streamlined navigation for opening and saving projects.

5. **Export Functionality**:
   - Export Gantt charts directly to PDF with user-defined file names.

---

## License

This project is licensed under the MIT License.

---

For more details, visit the [GitHub repository](https://github.com/MuhammedDemirtas/Gantt-Schedule-Chart-Planner).

