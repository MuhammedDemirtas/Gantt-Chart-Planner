# Gantt Schedule Chart Planner

This Python-based Gantt Chart Planner allows you to visualize and manage project schedules. It enables you to create tasks, define durations, set dependencies, and track progress in a Gantt chart format.
Features

    Create and edit tasks with start dates, durations, and dependencies.
    Visualize tasks and their dependencies in a Gantt chart.
    Save and load projects for continued work.

Installation

To install the necessary dependencies, clone this repository and install the required packages:
'''
git clone https://github.com/MuhammedDemirtas/Gantt-Schedule-Chart-Planner.git
cd Gantt-Schedule-Chart-Planner
'''
'''
pip install -r requirements.txt
'''

Running the Application

After installing the dependencies, you can run the application using:

python main.py

This will launch the Gantt chart planner, allowing you to define and manage your project tasks.

Code Overview

    main.py: The entry point of the application. It loads the interface and controls the overall project flow.
    gantt_chart.py: Handles the creation and visualization of the Gantt chart.
    task_manager.py: Manages task creation, task properties (such as start date, end date), and dependencies.
    utils.py: Contains utility functions for saving and loading projects.

License

This project is licensed under the MIT License.

For more details, visit the GitHub repository.
