import mysql.connector as C
import logging


class Mochi:
    def __init__(self):
        self.con = C.connect(database="mochi", autocommit=True)
        self.cur = self.con.cursor()
        self.logger = logging.getLogger("app.mochi")

    def new(self, name, description, author, url):
        command = f"INSERT INTO mochi VALUES (\"{name}\", \"{description}\", NOW(), \"{author}\", \"{url}\");"
        self.logger.info(f"New mochi entry created with '{command}'")
        self.cur.execute(command)

    def search_by_name(self, name):
        self.cur.execute(f"SELECT * FROM mochi WHERE name = \"{name}\";")
        return self.cur.fetchall()

    def search_by_author(self, author):
        self.cur.execute(f"SELECT * FROM mochi WHERE author = \"{author}\";")
        return self.cur.fetchall()

    def browse(self):
        self.cur.execute("SELECT * FROM mochi LIMIT 30;")
        return self.cur.fetchall()

    @staticmethod
    def reset():
        con = C.connect(database="mochi", autocommit=True)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS mochi;")
        cur.execute("CREATE TABLE mochi (name VARCHAR(255), description TEXT, date TIMESTAMP, author VARCHAR(255), url VARCHAR(255));")
        cur.close()
        con.close()

        logger = logging.getLogger("app.mochi")
        logger.warning("Mochi database RESET")


if __name__ == "__main__":
    pass
