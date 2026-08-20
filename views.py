from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Task, Action
from datetime import time, date, datetime
from sqlalchemy import func

views = Blueprint("views",__name__)

@views.route("/") 
@login_required
def home():
    tasks = db.session.query(Task, Action) \
    .join(Action, Task.action_id==Action.id) \
    .filter(Task.user_id==current_user.id, Task.is_deleted==False, 
            func.date(Task.created_at)==date.today())\
    .order_by(Task.status, Task.action_id, Task.deadline, Task.created_at) \
    .all()
    c_datetime = datetime.now()
    completed_len = len(Task.query.filter(Task.user_id==current_user.id, Task.status==True,
                        Task.is_deleted==False, 
                        func.date(Task.created_at)==c_datetime.date()).all())
    return render_template("home.html", n="2", css_filename="home.css", tasks=tasks, completed_len=completed_len, c_time=c_datetime.time())

@views.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        data = request.form
        if not all(data.values()):
            flash("All the fields are required!", "error")
        else: 
            action = Action.query.filter_by(name=data.get("action", "do")).first()
            task = Task(user_id=current_user.id,
                        action_id=action.id,
                        content=data.get("content"),
                        note=data.get("note"),
                        deadline=time.fromisoformat(data.get("deadline")))
            db.session.add(task)
            db.session.commit()
            flash("New task added successfully", "success")
            return redirect(url_for("views.home"))
    return render_template("edit.html", n="2", css_filename="edit.css", route="views.add", task="")

@views.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    task, action = None, None
    if request.method == "POST":
        data = request.form
        print(data)
        #try:
        task = Task.query.filter_by(id=data.get("task_id"), user_id=current_user.id).first()
        action = Action.query.filter_by(id=task.action_id).first()
        if len(data) > 1:
            if not all(data.values()):
                flash("All the fields are required!", "error")
            else:
                new_action = Action.query.filter_by(name=data.get("action")).first()
                task.action_id = new_action.id
                task.content = data.get("content")
                task.note = data.get("note")
                task.deadline = time.fromisoformat(data.get("deadline"))
                db.session.commit()
                flash("The task was edited successfully", "success")
                return redirect(url_for("views.home"))
        # except AttributeError:
        #     pass
    return render_template("edit.html", n="2", css_filename="edit.css", route="views.edit", task=task, action_name=action.name if action else "")

@views.route("/check", methods=["GET", "POST"])
@login_required
def check():
    if request.method == "POST":
        data = request.form
        try:
            task = Task.query.filter_by(id=data.get("task_id"), user_id=current_user.id).first()
            task.status = not task.status
            db.session.commit()
        except AttributeError:
            pass
    return redirect(url_for("views.home"))


@views.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        data = request.form
        try:
            task = Task.query.filter_by(id=data.get("task_id"), user_id=current_user.id).first()
            task.is_deleted = True
            db.session.commit()
        except AttributeError:
            pass
    return redirect(url_for("views.home"))

@views.route("/history") 
@login_required
def history():
    tasks = db.session.query(Task, Action).join(Action, Task.action_id==Action.id) \
    .filter(Task.user_id==current_user.id).order_by(Task.created_at.desc()) \
    .all()
    dates = db.session.query(func.date(Task.created_at))\
    .distinct() \
    .filter(Task.user_id == current_user.id) \
    .order_by(Task.created_at.desc()).all() 
    return render_template("history.html", n="2", css_filename="history.css", tasks=tasks, dates=[d[0] for d in dates])


@views.route("/search", methods=["GET", "POST"]) 
@login_required
def search():
    if request.method == "POST":
        search_q, date_q = request.form.get("search"), request.form.get("date")
        tasks = db.session.query(Task, Action).join(Action, Task.action_id==Action.id) \
        .filter(Task.user_id == current_user.id)
        if search_q:
            q = f"%{search_q}%"
            tasks = tasks.filter(Task.content.ilike(q))
        if date_q:
            tasks = tasks.filter(func.date(Task.created_at) == datetime.strptime(date_q, "%Y-%m-%d").date())
        dates = db.session.query(func.date(Task.created_at))\
        .distinct() \
        .filter(Task.user_id == current_user.id) \
        .order_by(Task.created_at.asc()).all() 
        return render_template("history.html", n="2", css_filename="history.css", tasks=tasks.all(), dates=[d[0] for d in dates])
    return redirect(url_for("views.history"))

@views.route("/back", methods=["GET", "POST"]) 
@login_required
def back():
    return redirect(url_for("views.history"))
