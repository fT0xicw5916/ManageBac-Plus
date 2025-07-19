import mysql.connector as C
import logging


class Notebooks:
    def __init__(self):
        self.con = C.connect(database="notebooks", autocommit=True)
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
        con = C.connect(database="notebooks", autocommit=True)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS notebooks;")
        cur.execute("CREATE TABLE notebooks (name VARCHAR(255), description TEXT, date TIMESTAMP, author VARCHAR(255), url VARCHAR(255));")
        cur.close()
        con.close()

        logger = logging.getLogger("app.notebooks")
        logger.warning("Notebooks database RESET")


if __name__ == "__main__":
    pass
