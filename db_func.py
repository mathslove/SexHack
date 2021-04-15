from datetime import datetime
from pathlib import Path
from sqlalchemy import and_
from config import resource
from models import *
import uuid
import shutil


def register_userDB(username, password):
    try:
        user = User(id=str(uuid.uuid4()), login=username, password=password)
        db.session.add(user)
        db.session.commit()
        token = str(user.id)
        return token
    except Exception as e:
        db.session.rollback()
        return None


def login_userDB(login, password):
    user = User.query.filter(and_(User.login == login, User.password == password)).first()
    if user is not None:
        return user.id
    else:
        return None


def get_all_themesDB():
    return Theme.query.all()


def add_themeDB(themeVal, img_link):
    try:
        themeT = Theme(theme=themeVal, svg_link=None)
        db.session.add(themeT)
        db.session.commit()

        themeT = Theme.query.filter_by(theme=themeVal).first()
        dir = Path(resource).joinpath("theme-{}.svg".format(themeT.id))
        shutil.copyfile(img_link, str(dir))

        Theme.query.filter_by(theme=themeVal).update({'svg_link': dir.name})
        db.session.commit()

        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


def add_taskDB(json_path, theme_id, inner_order, is_public=True, svg_path=None):
    try:
        json_f = open(json_path, "r")

        task = Task(task_json=json_f.read(), theme_id=theme_id, inner_order=inner_order,
                    is_public=is_public, svg_link=svg_path)
        db.session.add(task)
        db.session.commit()
        return True
    except Exception as e:
        return False


