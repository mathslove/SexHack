from datetime import datetime
from flask import Flask

app = Flask(__name__)


@app.route('/<login>&<password>', methods=["POST"])
def try_login(login, password):
    return True


@app.route('/time', methods=["GET"])
def time_check():
    return "{}".format(datetime.now())


if __name__ == '__main__':
    app.run()
