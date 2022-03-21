from utils import file_reader, timer


class ClickHouse:

    def __init__(self, cursor, file_name):
        self.cursor = cursor
        self.file_name = file_name

    @timer("ClickHouse", "Записано")
    def fill_table(self):
        sql = """INSERT INTO default.test (user_id, movie_id, viewed_frame) VALUES"""
        count = 0
        for row in file_reader(self.file_name):
            self.cursor.execute(sql, row)
            count += len(row)
        return count

    @timer("ClickHouse", "Прочитано")
    def select_from_table(self):
        sql = """SELECT * FROM default.test"""
        data = self.cursor.execute(sql)
        return len(data)
