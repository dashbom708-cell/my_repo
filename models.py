from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import func

db = SQLAlchemy()

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    tasks = db.relationship("Task")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey("action.id"), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    note = db.Column(db.String(10000), nullable=False)
    status = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
