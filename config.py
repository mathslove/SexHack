from sys import platform

if platform == "linux" or platform == "linux2":
    db_path = 'sqlite:////home/mika/resources/data/SexHack.sqlite'
    resource = r"/home/mika/resources/images"
elif platform == "win32":
    db_path = 'sqlite:///SexHack.sqlite'
    resource = r"C:\Users\mmas6\PycharmProjects\SexHack\static\images"


class Config:
    Debug = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = db_path
