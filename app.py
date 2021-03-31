from flask import Flask
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from models import db
migration = Migrate(app, db)

from views import *

if __name__ == '__main__':
    app.run()
    # app.run(host="0.0.0.0")