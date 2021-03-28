from datetime import datetime
from sqlite3 import IntegrityError
import os
from pathlib import Path
import shutil
from flask import Flask, request, send_file
import uuid
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SexHack.db'
resource = r"C:\Users\mmas6\PycharmProjects\SexHack\resource"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mika/resources/data/SexHack.db'
# resource = r"/home/mika/resources"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), unique=True, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    task_count = db.Column(db.TEXT, default="[]")


class Theme(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    theme = db.Column(db.TEXT, nullable=False, unique=True)
    jpeg_link = db.Column(db.TEXT)
    tasks = db.relationship('Task', backref='theme', lazy=True)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    task_json = db.Column(db.TEXT)
    jpeg_link = db.Column(db.TEXT)
    is_public = db.Column(db.BOOLEAN, default=True)
    theme_id = db.Column(db.TEXT, db.ForeignKey('theme.id'), nullable=False)
    inner_order = db.Column(db.Integer, nullable=False)


def register_userDB(login, password):
    try:
        user = User(id=str(uuid.uuid4()), login=login, password=password)
        db.session.add(user)
        db.session.commit()
        token = str(user.id)
        return token
    except Exception as e:
        db.session.rollback()
        print(e, file=open("debug.txt", "w"))
        return None


def login_userDB(login, password):
    user = User.query.filter_by(login=login).first()
    if user is not None and user.password == password:
        return user.id
    else:
        return None


def add_themeDB(themeVal, img_link):
    try:
        themeT = Theme(theme=themeVal, jpeg_link=None)
        db.session.add(themeT)
        db.session.commit()

        themeT = Theme.query.filter_by(theme=themeVal).first()
        res = Path(resource).joinpath("theme-{}.jpg".format(themeT.id))
        shutil.copyfile(img_link, str(res))
        Theme.query.filter_by(theme=themeVal).update({'jpeg_link': res.name})
        db.session.commit()

        return True
    except Exception as e:
        print(e)
        return False


def add_taskDB(json_path, theme_id, inner_order, is_public=True, jpeg_path=None):
    try:
        json_f = open(json_path, "r")

        task = Task(task_json=json_f.read(), theme_id=theme_id, inner_order=inner_order,
                    is_public=is_public, jpeg_link=jpeg_path)
        db.session.add(task)
        db.session.commit()
        return True
    except Exception as e:
        return False


@app.route('/login', methods=['POST'])
def login():
    req_json = request.get_json()
    token = login_userDB(req_json['login'], req_json['password'])
    if token is not None:
        return json.dumps({'token': token }, indent=4)
    else:
        return json.dumps({'error': 'login was failed'}, indent=4)


@app.route('/register', methods=['POST'])
def register_user():
    req_json = request.get_json()
    token = register_userDB(req_json["login"], req_json["password"])
    if token is not None:
        return json.dumps({'token': token}, indent=4)
    else:
        return json.dumps({'error': 'register was failed'}, indent=4)


@app.route('/themes', methods=['GET'])
def get_all_themes():
    themes = Theme.query.all()
    d = {}
    for theme in themes:
        d[theme.theme] = dict()
        d[theme.theme]["id"] = theme.id
        d[theme.theme]["jpeg_link"] = "/download/{}".format(theme.jpeg_link)
    print(d)
    print(json.dumps(d, indent=4))
    return json.dumps(d, indent=4)


@app.route('/download/<filename>', methods=["GET"])
def download(filename):
    return send_file(Path(resource).joinpath(filename))


@app.route('/time', methods=["GET"])
def time_check():
    return "{}".format(datetime.now())


if __name__ == '__main__':
    app.run()
    # app.run(host="0.0.0.0")