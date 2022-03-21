import csv
from functools import wraps
from time import time


def timer(database, operation):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time()
            count = func(*args, **kwargs)
            result_time = time() - start

            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f"{operation} {count} записей в {database} за {result_time} \n")

        return wrapper

    return decorator


def file_reader(file_name):
    with open(file_name, "r") as csvfile:
        datareader = csv.reader(csvfile)
        _ = next(datareader)  # Header
        size = 1000
        count = 0
        data = []

        for row in datareader:
            if count >= size:
                count = 0
                yield data

            data.append((int(row[0]), row[1], int(row[2])))
            count += 1
