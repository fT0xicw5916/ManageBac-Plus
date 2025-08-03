import mysql.connector as C
import logging
import os


class Notebooks:
    def __init__(self):
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_port = os.environ.get("db_port")

        if db_username is None or db_password is None or db_port is None:
            self.con = C.connect(database="notebooks", autocommit=True)
        else:
            self.con = C.connect(database="notebooks", autocommit=True, user=db_username, password=db_password, port=db_port)
        self.cur = self.con.cursor()
        self.logger = logging.getLogger("app.notebooks")

    def new(self, name, description, author, url):
        command = f"INSERT INTO notebooks VALUES (\"{name}\", \"{description}\", NOW(), \"{author}\", \"{url}\");"
        self.logger.info(f"New notebooks entry created with '{command}'")
        self.cur.execute(command)

    def browse(self):
        self.cur.execute("SELECT * FROM notebooks;")
        return self.cur.fetchall()

    @staticmethod
    def reset():
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_port = os.environ.get("db_port")

        if db_username is None or db_password is None or db_port is None:
            con = C.connect(database="notebooks", autocommit=True)
        else:
            con = C.connect(database="notebooks", autocommit=True, user=db_username, password=db_password, port=db_port)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS notebooks;")
        cur.execute("CREATE TABLE notebooks (name VARCHAR(255), description TEXT, date TIMESTAMP, author VARCHAR(255), url VARCHAR(255));")
        cur.close()
        con.close()

        logger = logging.getLogger("app.notebooks")
        logger.warning("Notebooks database RESET")


if __name__ == "__main__":
    pass
