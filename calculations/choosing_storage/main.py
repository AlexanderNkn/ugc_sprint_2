from time import sleep

import vertica_python
from clickhouse_driver import Client

from click_house import ClickHouse
from settings import vetrica_info
from vetica import Vetrica

if __name__ == '__main__':
    results = {}
    with vertica_python.connect(**vetrica_info) as connection:
        vetrica_cursor = connection.cursor()
        ch_cursor = Client(host='localhost')
        file_with_test_data = "test_data.csv"
        databases = (Vetrica(vetrica_cursor, file_with_test_data), ClickHouse(ch_cursor, file_with_test_data))

        for database in databases:
            database.fill_table()
            sleep(5)  # ClickHouse не сразу подтягивает записанные данные
            database.select_from_table()



