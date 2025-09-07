import mysql.connector as C
import logging
import os


class Scores:
    def __init__(self):
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_port = os.environ.get("db_port")

        if db_username is None or db_password is None or db_port is None:
            self.con = C.connect(database="scores", autocommit=True)
        else:
            self.con = C.connect(database="scores", autocommit=True, user=db_username, password=db_password, port=int(db_port))
        self.cur = self.con.cursor()
        self.logger = logging.getLogger("app.scores")

    def new_class(self, name: str, weights):
        w = ""
        for weight in weights:
            w += '`' + weight + '`' + " FLOAT(24), "
        if w == "":
            command = f"CREATE TABLE `{name}` (id int, Overall FLOAT(24));"
        else:
            command = f"CREATE TABLE `{name}` (id int, Overall FLOAT(24), {w[:-2]});"
        self.logger.info(f"New class table created with '{command}'")
        self.cur.execute(command)

    def check_class(self, name):
        self.cur.execute(f"SHOW TABLES LIKE \"{name}\";")
        return False if len(self.cur.fetchall()) == 0 else True

    def new_score(self, id, c, s):
        data = ""
        for i in s:
            if i is None:
                data += "NULL, "
                continue
            data += str(i) + ", "
        command = f"INSERT INTO `{c}` VALUES ({id}, {data[:-2]});"
        self.logger.info(f"New score entry created with '{command}'")
        self.cur.execute(command)

    def search_score(self, id, c):
        self.cur.execute(f"SELECT * FROM `{c}` WHERE id = {id};")
        return self.cur.fetchall()

    def get_category_score(self, id, class_name):
        scores = self.search_score(id, class_name)[0]
        categories = [i[0] for i in self.get_weight_names(class_name)]
        results = {}
        for i, c in enumerate(categories):
            results[c] = scores[i]
        return results

    def get_weight_names(self, c):
        self.cur.execute(f"SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = \"scores\" AND table_name = \"{c}\";")
        return self.cur.fetchall()

    @staticmethod
    def reset():
        db_username = os.environ.get("db_username")
        db_password = os.environ.get("db_password")
        db_port = os.environ.get("db_port")

        if db_username is None or db_password is None or db_port is None:
            con = C.connect(autocommit=True)
        else:
            con = C.connect(autocommit=True, user=db_username, password=db_password, port=int(db_port))
        cur = con.cursor()
        cur.execute("DROP DATABASE IF EXISTS scores;")
        cur.execute("CREATE DATABASE scores;")
        cur.close()
        con.close()

        logger = logging.getLogger("app.scores")
        logger.warning("Scores database RESET")


if __name__ == "__main__":
    pass
