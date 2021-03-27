from datetime import datetime
from flask import Flask
import uuid
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SexHack.db'
app.config['SERVER_NAME'] = '0.0.0.0'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), unique=True, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    task_count = db.Column(db.TEXT, default="[]")


def register_user(login, password):
    user = User(id=str(uuid.uuid4()), login=login, password=password)
    db.session.add()
    db.session.commit()
    d = {'Token', str(user.id)}
    return "{ 'Token' = '{}'}".format(str(user.id))


def login_user(login, password):
    pass


@app.route('/login/login=<login>&password=<password>', methods=["POST"])
def login(login, password):
    token = login(login, password)


@app.route('/register/login=<login>&password=<password>', methods=["POST"])
def register_user(login, password):
    register_user(login, password)


@app.route('/time', methods=["GET"])
def time_check():
    return "{}".format(datetime.now())


if __name__ == '__main__':
    app.run()
