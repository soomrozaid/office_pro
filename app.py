from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# Dummy data
areas = []
tasks = []


@app.route("/")
def index():
    today = datetime.today().strftime("%Y-%m-%d")
    daily_tasks = [
        task
        for task in tasks
        if task["due_date"] == today and not task.get("completed")
    ]
    sorted_tasks = sorted(
        daily_tasks,
        key=lambda x: [
            "Must Do Today",
            "Should Do Today",
            "Could Do Today",
            "Nice to Do Today",
        ].index(x["priority"]),
    )
    return render_template(
        "index.html", areas=areas, tasks=tasks, daily_tasks=sorted_tasks
    )


@app.route("/add_area", methods=["POST"])
def add_area():
    area_name = request.form.get("area_name")
    time_commitment = request.form.get("time_commitment")
    areas.append(
        {"name": area_name, "time_commitment": time_commitment, "projects": []}
    )
    return redirect(url_for("index"))


@app.route("/add_project", methods=["POST"])
def add_project():
    project_name = request.form.get("project_name")
    area_id = int(request.form.get("area_id"))
    project = {"name": project_name, "tasks": []}
    areas[area_id]["projects"].append(project)
    return redirect(url_for("index"))


@app.route("/add_task", methods=["POST"])
def add_task():
    task_name = request.form.get("task_name")
    due_date = request.form.get("due_date")
    priority = request.form.get("priority")
    project_id = int(request.form.get("project_id"))
    task = {
        "name": task_name,
        "due_date": due_date,
        "priority": priority,
        "completed": False,
    }
    tasks.append(task)
    for area in areas:
        for project in area["projects"]:
            if project == area["projects"][project_id]:
                project["tasks"].append(task)
    return redirect(url_for("index"))


@app.route("/edit_task/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    task = tasks[task_id]
    task["name"] = request.form.get("task_name")
    task["due_date"] = request.form.get("due_date")
    task["priority"] = request.form.get("priority")
    return redirect(url_for("index"))


@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = tasks.pop(task_id)
    for area in areas:
        for project in area["projects"]:
            if task in project["tasks"]:
                project["tasks"].remove(task)
    return redirect(url_for("index"))


@app.route("/complete_task/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    tasks[task_id]["completed"] = not tasks[task_id]["completed"]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
