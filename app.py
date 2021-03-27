from datetime import datetime
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
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    task_count = db.Column(db.TEXT, default="[]")


def register_userDB(login, password):
    user = User(id=str(uuid.uuid4()), login=login, password=password)
    db.session.add(user)
    db.session.commit()
    token = str(user.id)
    return token


def login_user(login, password):
    pass


@app.route('/login', methods=["POST"])
def login(username, password):
    token = login(username, password)


@app.route('/register', methods=['POST'])
def register_user():
    req_json = request.get_json()
    d = {'token' : register_userDB(req_json["login"], req_json["password"])}
    return json.dumps(d, indent=10)


@app.route('/time', methods=["GET"])
def time_check():
    return "{}".format(datetime.now())


if __name__ == '__main__':
    app.run()
