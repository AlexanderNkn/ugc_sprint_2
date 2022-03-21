from utils import timer, file_reader


class Vetrica:

    def __init__(self, cursor, file_name):
        self.cursor = cursor
        self.file_name = file_name
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS views 
            (id IDENTITY,
            user_id INTEGER NOT NULL,
            movie_id VARCHAR(256) NOT NULL,
            viewed_frame INTEGER NOT NULL
        );""")

    @timer("Vetrica", "Записано")
    def fill_table(self):
        count = 0
        sql = """INSERT INTO views (user_id, movie_id, viewed_frame) VALUES (%s, %s, %s); """
        for row in file_reader(self.file_name):
            self.cursor.executemany(sql, row)
            count += len(row)
        return count

    @timer("Vetrica", "Прочитано")
    def select_from_table(self):
        sql = """SELECT user_id, movie_id, viewed_frame FROM views;"""
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return len(data)
