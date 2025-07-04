import mysql.connector as C
import logging


class Scores:
    def __init__(self):
        self.con = C.connect(database="scores", autocommit=True)
        self.cur = self.con.cursor()
        self.logger = logging.getLogger("app.scores")

    def new_class(self, name: str, weights):
        w = ""
        for weight in weights:
            w += '`' + weight + '`' + " FLOAT(24), "
        command = f"CREATE TABLE `{name}` (id int, Overall FLOAT(24), {w[:-2]});"
        self.cur.execute(command)
        self.logger.info(f"New class table created with '{command}'")

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
        self.cur.execute(command)
        self.logger.info(f"New score entry created with '{command}'")

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
        con = C.connect(database="scores", autocommit=True)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS a;")
        cur.execute("DROP TABLE IF EXISTS b;")
        cur.execute("DROP TABLE IF EXISTS credentials;")
        cur.execute("DROP TABLE IF EXISTS Advanced_Comprehensive_English_Grade_10_5;")
        cur.execute("DROP TABLE IF EXISTS Economics_Honor_Grade_10_1 ;")
        cur.execute("DROP TABLE IF EXISTS Introduction_to_Language_and_Literature_Grade_10_7;")
        cur.execute("DROP TABLE IF EXISTS PE4_Grade_10_41;")
        cur.execute("DROP TABLE IF EXISTS Physics_Honor_Grade_10_3;")
        cur.execute("DROP TABLE IF EXISTS PreCalculus_Extended_Grade_10_6;")
        cur.close()
        con.close()

        logger = logging.getLogger("app.scores")
        logger.warning("Scores database RESET")


if __name__ == "__main__":
    pass
