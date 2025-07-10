import mysql.connector as C
import logging


class Credentials:
    def __init__(self):
        self.con = C.connect(database="credentials", autocommit=True)
        self.cur = self.con.cursor()
        self.logger = logging.getLogger("app.credentials")

    def new(self, email, password, microsoft, classes):
        s = ""
        for c in classes:
            s += '\"' + c + "\", "
        command = f"INSERT INTO credentials VALUES (0, \"{email}\", \"{password}\", {microsoft}, {s[:-2]});"
        self.logger.info(f"New credentials entry created with '{command}'")
        self.cur.execute(command)

    def search(self, email):
        self.cur.execute(f"SELECT * FROM credentials WHERE email = \"{email}\";")
        return self.cur.fetchall()

    def browse(self):
        self.cur.execute("SELECT * FROM credentials;")
        res = []
        for i in self.cur.fetchall():
            res.append([i[1], i[2], i[3]])
        return res

    @staticmethod
    def reset():
        con = C.connect(database="credentials", autocommit=True)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS credentials;")
        cur.execute("CREATE TABLE credentials (id int NOT NULL AUTO_INCREMENT, email VARCHAR(255), password VARCHAR(255), microsoft TINYINT, class1 VARCHAR(255), class2 VARCHAR(255), class3 VARCHAR(255), class4 VARCHAR(255), class5 VARCHAR(255), class6 VARCHAR(255), class7 VARCHAR(255), PRIMARY KEY (id));")
        cur.close()
        con.close()

        logger = logging.getLogger("app.credentials")
        logger.warning("Credentials database RESET")


if __name__ == "__main__":
    pass
