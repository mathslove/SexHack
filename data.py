import sqlite3
import uuid


class user:
    def __init__(self, login, password):
        self.info = {
            'login': login,
            'password': password,
            'uuid': str(int(uuid.uuid4())),
        }


class task:
    def __init__(self, content=None):
        self.info = {
            'content': content
        }


class users:
    def __init__(self, parentDB, signature):
        self.size = 0
        self.parent = parentDB
        self.cursor = self.parent.cursor()
        self.insSign = ", ".join(signature.info.keys())

        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS users(login, password, uuid);")
        self.parent.commit()

    def update(self):
        self.cursor.execute("DROP TABLE IF EXISTS users")
        self.parent.commit()

    def addUser(self, user):
        arr = [_ for _ in user.info.values()]
        self.cursor.execute("INSERT INTO users(login, password, uuid) VALUES(?,?,?);", arr)
        self.parent.commit()

    def LogIn(self, login, password):
        str = f"SELECT * FROM users where login='{login}' AND password='{password}';"
        # print(str)
        callback = self.cursor.execute(str)
        t = callback.fetchone()[2]
        return t

    def findBySignature(self, userSiganature):
        dict = {}
        for i, j in userSiganature.info.items():
            if j is not None and j is not "":
                dict[i] = j
        if len(dict) is 0:
            print(self.cursor.execute("SELECT * FROM users").fetchall())
        else:
            request = " AND ".join([f"{key}='{value}'" for key, value in dict.items()])
            print(request)


class tasks:
    def __init__(self, parentDB, signature):
        self.parent = parentDB
        self.cursor = self.parent.cursor()
        self.insSign = ", ".join(signature.info.keys())

        sign = " TEXT,".join(signature.info.keys()) + " TEXT"

        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(task_id INTEGER PRIMARY KEY, " + sign + ");")
        self.parent.commit()

    def addTask(self, text):
        arr = [_ for _ in user.info.values()]
        str = "?, " * (len(arr) - 1) + "?"
        self.cursor.execute(f"INSERT INTO tasks('{self.insSign}') VALUES('{str}');", arr)
        self.parent.commit()

    def update(self):
        self.cursor.execute("DROP TABLE IF EXISTS tasks")
        self.parent.commit()


conn = sqlite3.connect('test.sqlite')

#usersDB = users(conn, user("", ""))

#usersDB.addUser(user("lolilover", "123"))
#usersDB.LogIn("vas9", "kamen")
