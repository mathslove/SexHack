from datetime import datetime
from sqlite3 import IntegrityError

from flask import Flask, request
import uuid
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SexHack.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), unique=True, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    task_count = db.Column(db.TEXT, default="[]")


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
    if user.password == password:
        return user.id
    else:
        return None


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
        return json.dumps({'token', token}, indent=4)
    else:
        return json.dumps({'error': 'register was failed'}, indent=4)


@app.route('/time', methods=["GET"])
def time_check():
    return "{}".format(datetime.now())


if __name__ == '__main__':
    app.run()
