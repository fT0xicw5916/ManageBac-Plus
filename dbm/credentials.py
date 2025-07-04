import mysql.connector as C
import logging


class Credentials:
    def __init__(self):
        self.con = C.connect(database="credentials", autocommit=True)
        self.cur = self.con.cursor()
        self.logger = logging.getLogger(__name__)

    def new(self, email, password, classes):
        s = ""
        for c in classes:
            s += '\"' + c + "\", "
        command = f"INSERT INTO credentials VALUES (0, \"{email}\", \"{password}\", {s[:-2]});"
        self.cur.execute(command)
        self.logger.info(f"New credentials entry created with '{command}'")

    def search(self, email):
        self.cur.execute(f"SELECT * FROM credentials WHERE email = \"{email}\";")
        return self.cur.fetchall()

    @staticmethod
    def reset():
        con = C.connect(database="credentials", autocommit=True)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS credentials;")
        cur.execute("CREATE TABLE credentials (id int NOT NULL AUTO_INCREMENT, email VARCHAR(255), password VARCHAR(255), class1 VARCHAR(255), class2 VARCHAR(255), class3 VARCHAR(255), class4 VARCHAR(255), class5 VARCHAR(255), class6 VARCHAR(255), class7 VARCHAR(255), PRIMARY KEY (id));")
        cur.close()
        con.close()

        logger = logging.getLogger(__name__)
        logger.warning("Credentials database RESET")


if __name__ == "__main__":
    pass
