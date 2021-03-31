from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), unique=True, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)


class UserDetails(db.Model):
    __tablename__ = "users_details"
    id = db.Column(db.String(36), unique=True, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    first_name = db.Column(db.TEXT)
    last_name = db.Column(db.TEXT)
    age = db.Column(db.Integer)
    task_count = db.Column(db.TEXT, default="[]")


class Theme(db.Model):
    __tablename__ = 'themes'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.TEXT, nullable=False, unique=True)
    svg_link = db.Column(db.TEXT)
    tasks = db.relationship('Task', backref='themes', lazy=True)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    task_json = db.Column(db.TEXT)
    svg_link = db.Column(db.TEXT)
    is_public = db.Column(db.BOOLEAN, default=True)
    theme_id = db.Column(db.TEXT, db.ForeignKey('themes.id'), nullable=False)
    inner_order = db.Column(db.Integer, nullable=False)
