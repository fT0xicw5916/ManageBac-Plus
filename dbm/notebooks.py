import mysql.connector as C


class Notebooks:
    def __init__(self):
        self.con = C.connect(database="notebooks", autocommit=True)
        self.cur = self.con.cursor()

    def new(self, name, description, author, url):
        self.cur.execute(f"INSERT INTO notebooks VALUES (\"{name}\", \"{description}\", NOW(), \"{author}\", \"{url}\");")

    def search_by_name(self, name):
        self.cur.execute(f"SELECT * FROM notebooks WHERE name = \"{name}\";")
        return self.cur.fetchall()

    def search_by_author(self, author):
        self.cur.execute(f"SELECT * FROM notebooks WHERE author = \"{author}\";")
        return self.cur.fetchall()

    def browse(self):
        self.cur.execute("SELECT * FROM notebooks LIMIT 30;")
        return self.cur.fetchall()

    @staticmethod
    def reset():
        con = C.connect(database="notebooks", autocommit=True)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS notebooks;")
        cur.execute("CREATE TABLE notebooks (name VARCHAR(255), description TEXT, date TIMESTAMP, author VARCHAR(255), url VARCHAR(255));")
        cur.close()
        con.close()


if __name__ == "__main__":
    pass
