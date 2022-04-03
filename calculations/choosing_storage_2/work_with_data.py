import os
import pandas as pd

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def users_data_fname(dirname):
    return os.path.join(dirname, 'data', 'users.csv')


def movies_data_fname(dirname):
    return os.path.join(dirname, 'data', 'movies.csv')


def reviews_data_fname(dirname):
    return os.path.join(dirname, 'data', 'reviews.csv')


def generate_users(fname, records=100):
    import uuid

    if os.path.isdir(fname):
        fname = users_data_fname(fname)

    with open(fname, 'w') as f_out:
        f_out.write('user_id')
        for record_num in range(records):
            f_out.write('\n')
            f_out.write(str(uuid.uuid4()))


def generate_movies(fname, records=100):
    import uuid

    if os.path.isdir(fname):
        fname = movies_data_fname(fname)

    with open(fname, 'w') as f_out:
        f_out.write('movie_id')
        for record_num in range(records):
            f_out.write('\n')
            f_out.write(str(uuid.uuid4()))


def read_users(fname):
    if os.path.isdir(fname):
        fname = users_data_fname(fname)
    df = pd.read_csv(fname, sep=';')
    return df.user_id.values


def read_movies(fname):
    if os.path.isdir(fname):
        fname = movies_data_fname(fname)
    df = pd.read_csv(fname, sep=';')
    return df.movie_id.values


def read_reviews(fname):
    if os.path.isdir(fname):
        fname = reviews_data_fname(fname)
    df = pd.read_csv(fname, sep=';')
    return df.review.values


if __name__ == '__main__':
    generate_users(users_data_fname(ROOT_DIR), records=200000)
    generate_movies(movies_data_fname(ROOT_DIR), records=5000)
