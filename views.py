from app import app
from config import resource
from db_func import *
from flask import request, send_file
import json
from pathlib import Path
from datetime import datetime


@app.route('/login', methods=['POST'])
def login():
    req_json = request.get_json()
    token = login_userDB(req_json['login'], req_json['password'])
    if token is not None:
        return json.dumps({'token': token}, indent=4)
    else:
        return json.dumps({'error': 'Login was failed'}, indent=4)


@app.route('/register', methods=['POST'])
def register_user():
    req_json = request.get_json()
    token = register_userDB(req_json["login"], req_json["password"])
    if login_userDB(req_json["login"], req_json["password"]):
        return json.dumps({'error': 'User already exists!'}, indent=4)
    if token is None:
        return json.dumps({'error': 'Register was failed!'}, indent=4)
    else:
        return json.dumps({'token': token}, indent=4)


@app.route('/themes', methods=['GET'])
def get_all_themes():
    themes = get_all_themesDB()
    d = dict()
    for theme in themes:
        d[theme.theme] = dict()
        d[theme.theme]["id"] = theme.id
        d[theme.theme]["svg_link"] = "/download/{}".format(theme.svg_link)
    return json.dumps(d, indent=4)


@app.route('/download/<filename>', methods=["GET"])
def download(filename):
    return send_file(Path(resource).joinpath(filename))


@app.route('/time', methods=["GET"])
def time_check():
    return "{}".format(datetime.now())
