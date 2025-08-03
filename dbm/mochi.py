import mysql.connector as C
import logging
import os


class Mochi:
    def __init__(self):
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_port = os.environ.get("db_port")

        if db_username is None or db_password is None or db_port is None:
            self.con = C.connect(database="mochi", autocommit=True)
        else:
            self.con = C.connect(database="mochi", autocommit=True, user=db_username, password=db_password, port=db_port)
        self.cur = self.con.cursor()
        self.logger = logging.getLogger("app.mochi")

    def new(self, name, description, author, url):
        command = f"INSERT INTO mochi VALUES (\"{name}\", \"{description}\", NOW(), \"{author}\", \"{url}\");"
        self.logger.info(f"New mochi entry created with '{command}'")
        self.cur.execute(command)

    def browse(self):
        self.cur.execute("SELECT * FROM mochi;")
        return self.cur.fetchall()

    @staticmethod
    def reset():
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_port = os.environ.get("db_port")

        if db_username is None or db_password is None or db_port is None:
            con = C.connect(database="mochi", autocommit=True)
        else:
            con = C.connect(database="mochi", autocommit=True, user=db_username, password=db_password, port=db_port)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS mochi;")
        cur.execute("CREATE TABLE mochi (name VARCHAR(255), description TEXT, date TIMESTAMP, author VARCHAR(255), url VARCHAR(255));")
        cur.close()
        con.close()

        logger = logging.getLogger("app.mochi")
        logger.warning("Mochi database RESET")


if __name__ == "__main__":
    pass
