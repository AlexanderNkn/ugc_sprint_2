import os

import pandas as pd
import pymongo
import numpy as np
import time
import tqdm
import datetime
import pprint

import logging
from logging import config

from logging_config import LOGGING_CONFIG
from settings import MONGO_HOST, MONGO_PORT

import work_with_data

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('choosing_storage_mongo')


def generate_movie_likes(db, random_seed=None, bulk_size=10_000, samples=10_000_000) -> None:
    test_movie_likes = db.test_movie_likes

    if random_seed:
        np.random.seed(random_seed)

    users = work_with_data.read_users(work_with_data.ROOT_DIR)
    movies = work_with_data.read_movies(work_with_data.ROOT_DIR)
    likes = [True, False]

    for _ in tqdm.tqdm(range(samples // bulk_size)):
        batch_users = np.random.choice(users, bulk_size)
        batch_movies = np.random.choice(movies, bulk_size)
        batch_like = np.random.choice(likes, bulk_size)

        new_posts = [{
            'user_id': user_id,
            'movie_id': movie_id,
            'like': bool(like),
        } for user_id, movie_id, like in zip(batch_users, batch_movies, batch_like)]
        result = test_movie_likes.insert_many(new_posts)


def generate_movie_reviews(db, random_seed=None, bulk_size=10_000, samples=5_000_000) -> None:
    test_movie_reviews = db.test_movie_reviews

    if random_seed:
        np.random.seed(random_seed)

    users = work_with_data.read_users(work_with_data.ROOT_DIR)
    movies = work_with_data.read_movies(work_with_data.ROOT_DIR)
    reviews = work_with_data.read_reviews(work_with_data.ROOT_DIR)
    batches = max(samples // bulk_size, 1)

    for _ in tqdm.tqdm(range(batches)):
        batch_users = np.random.choice(users, bulk_size)
        batch_movies = np.random.choice(movies, bulk_size)
        batch_reviews = np.random.choice(reviews, bulk_size)

        new_posts = [{
            'user_id': user_id,
            'movie_id': movie_id,
            'review_text': review,
        } for user_id, movie_id, review in zip(batch_users, batch_movies, batch_reviews)]
        result = test_movie_reviews.insert_many(new_posts)


def generate_movie_bookmarks(db, random_seed=None, bulk_size=10_000, max_bookmarks=20) -> None:
    test_user_bookmarks = db.test_user_bookmarks

    if random_seed:
        np.random.seed(random_seed)

    users = work_with_data.read_users(work_with_data.ROOT_DIR)
    movies = work_with_data.read_movies(work_with_data.ROOT_DIR)

    # среднее число записей на пользователя ~10, тогда берем 1000 пользователей для 10_000 записей в bulk
    chunk_size = bulk_size // (max_bookmarks / 2)
    batches = max(len(users) // chunk_size, 1)

    for users_subarray in tqdm.tqdm(np.array_split(users, batches)):

        batch_users = np.repeat(users_subarray, np.random.choice(range(max_bookmarks), users_subarray.shape))
        batch_movies = np.random.choice(movies, batch_users.shape)

        new_posts = [{
            'user_id': user_id,
            'movie_id': movie_id,
        } for user_id, movie_id in zip(batch_users, batch_movies)]
        result = test_user_bookmarks.insert_many(new_posts)


def aggregate_user_likes(db, random_seed=None, test_count=10):
    if random_seed:
        np.random.seed(random_seed)

    times = []

    users = work_with_data.read_users(work_with_data.ROOT_DIR)
    users = np.random.choice(users, test_count)
    for user_id in users:
        time_1 = time.perf_counter()

        result = db.test_movie_likes.aggregate([
            {
                '$match': {
                    'user_id': user_id
                }
            },
            {
                '$match': {
                    'like': True
                }
            },
            {
                '$group': {
                    '_id': {
                        'user_id': '$user_id'
                    },
                    'movies_id': {
                        '$push': '$movie_id'
                    },
                }
            }
        ])
        for batch in result:
            movies = batch['movies_id']

        time_2 = time.perf_counter()
        times.append(time_2 - time_1)

    return times


def aggregate_movies_likes(db, random_seed=None, test_count=10):
    if random_seed:
        np.random.seed(random_seed)

    times = []

    movies = work_with_data.read_movies(work_with_data.ROOT_DIR)
    movies = np.random.choice(movies, test_count)
    for movie_id in movies:
        time_1 = time.perf_counter()

        result = db.test_movie_likes.aggregate([
            {
                '$match': {
                    'movie_id': movie_id
                }
            },
            {
                '$group': {
                    '_id': {
                        'movie_id': '$movie_id'
                    },
                    'likes': {
                        '$sum': {
                            '$cond': {'if': {'$eq': ['$like', True]}, 'then': 1, 'else': 0}
                        }
                    },
                    'dislikes': {
                        '$sum': {
                            '$cond': {'if': {'$eq': ['$like', False]}, 'then': 1, 'else': 0}
                        }
                    }
                }
            }
        ])
        for batch in result:
            likes = batch['likes']
            dislikes = batch['dislikes']
            rating = likes / (likes + dislikes) * 10 if likes + dislikes else None

        time_2 = time.perf_counter()
        times.append(time_2 - time_1)

    return times


def aggregate_bookmarks(db, random_seed=None, test_count=10):
    if random_seed:
        np.random.seed(random_seed)

    times = []

    users = work_with_data.read_users(work_with_data.ROOT_DIR)
    users = np.random.choice(users, test_count)
    for user_id in users:
        time_1 = time.perf_counter()

        result = db.test_user_bookmarks.aggregate([
            {
                '$match': {
                    'user_id': user_id
                }
            },
            {
                '$group': {
                    '_id': {
                        'user_id': '$user_id'
                    },
                    'movies_id': {
                        '$push': '$movie_id'
                    },
                }
            }
        ])
        for batch in result:
            movies = batch['movies_id']

        time_2 = time.perf_counter()
        times.append(time_2 - time_1)

    return times


def records_count(db) -> None:
    filter = {"name": {"$regex": r"^(?!system\.)"}}
    collections = db.list_collection_names(filter=filter)
    collections_records_count = {}
    for col in collections:
        collections_records_count[col] = db[col].count_documents(filter={})

    return collections_records_count


def remove_test_collections(db) -> None:
    filter = {"name": {"$regex": r"^(?!system\.)"}}
    collections = db.list_collection_names(filter=filter)
    for col in collections:
        db.drop_collection(db[col])


def prepare_collections(db, use_indexes=True):
    test_movie_likes = db.test_movie_likes
    test_movie_reviews = db.test_movie_reviews
    test_user_bookmarks = db.test_user_bookmarks
    if use_indexes:
        test_movie_likes.create_index([("user_id", 1)])
        test_movie_likes.create_index([("movie_id", 1)])
        test_movie_reviews.create_index([("movie_id", 1)])
        test_user_bookmarks.create_index([("user_id", 1)])
    else:
        test_movie_likes.drop_indexes()
        test_movie_reviews.drop_indexes()
        test_user_bookmarks.drop_indexes()


def log_generate_time(log_file, db, collection_name, generate_time):
    samples = db[collection_name].count_documents(filter={})
    log_file.write(f'{collection_name:20}\t')
    log_file.write(f'{samples:10}\t')
    log_file.write(f'{generate_time:10.4}\t')
    time_per_sample = (generate_time / samples) * 1000 if samples else '-'
    log_file.write(f'{time_per_sample:10.4}\n')


def log_aggregate_time(log_file, aggregate_name, aggregate_time):
    df = pd.DataFrame(aggregate_time, columns=['time'])
    df['time'] = df['time'] * 1000

    log_file.write(aggregate_name + '\n')

    pprint.pprint(df.describe(), stream=log_file)
    log_file.write('\n')


def measure_time(db, use_indexes):

    result_dir = os.path.join(work_with_data.ROOT_DIR, 'results')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir, exist_ok=True)

    remove_test_collections(db)
    prepare_collections(db, use_indexes=use_indexes)

    random_seed = 42

    bulk_size = 10_000
    movie_likes_samples = 10_000_000
    movie_reviews_samples = 5_000_000
    users_max_bookmarks = 20

    test_count = 100

    log_time = datetime.datetime.now().isoformat(timespec='seconds')
    log_name = log_time.replace(':', '') + '.txt'
    log_name = os.path.join(result_dir, log_name)
    with open(log_name, 'w') as log_file:
        log_file.write(f'start time: {log_time}\n')

        users = work_with_data.read_users(work_with_data.ROOT_DIR)
        movies = work_with_data.read_movies(work_with_data.ROOT_DIR)
        reviews = work_with_data.read_reviews(work_with_data.ROOT_DIR)

        log_file.write(f'Users count: {len(users)}\n')
        log_file.write(f'Movies count: {len(movies)}\n')
        log_file.write(f'Reviews count: {len(reviews)}\n')
        log_file.write('\n')

        if use_indexes:
            log_file.write('Use indexes for user_id and movie_id\n')
        else:
            log_file.write('Indexes don\'t use\n')
        log_file.write(f'bulk_size: {bulk_size}\n')
        log_file.write(f'users max_bookmarks: {users_max_bookmarks}\n')

        log_file.write(f'movie_likes samples: {movie_likes_samples}\n')
        log_file.write(f'movie_reviews samples: {movie_reviews_samples}\n')
        log_file.write('\n')

        log_file.write('Time for generate collection:\n')
        log_file.write('-' * 100 + '\n')
        log_file.write('Collection          \tsamples   \ttime(s)   \ttime_per_sample(ms)\n')

        time_start = time.perf_counter()
        generate_movie_likes(db, random_seed=random_seed, bulk_size=bulk_size, samples=movie_likes_samples)
        time_end = time.perf_counter()
        log_generate_time(log_file, db, 'test_movie_likes', time_end - time_start)

        time_start = time.perf_counter()
        generate_movie_reviews(db, random_seed=random_seed, bulk_size=bulk_size, samples=movie_reviews_samples)
        time_end = time.perf_counter()
        log_generate_time(log_file, db, 'test_movie_reviews', time_end - time_start)

        time_start = time.perf_counter()
        generate_movie_bookmarks(db, random_seed=random_seed, bulk_size=bulk_size, max_bookmarks=users_max_bookmarks)
        time_end = time.perf_counter()
        log_generate_time(log_file, db, 'test_user_bookmarks', time_end - time_start)

        log_file.write('\nTime for aggregate operation (ms):\n\n')

        times = aggregate_movies_likes(db, random_seed=random_seed, test_count=test_count)
        log_aggregate_time(log_file, 'Get movies ranking', times)

        times = aggregate_user_likes(db, random_seed=random_seed, test_count=test_count)
        log_aggregate_time(log_file, 'Get users likes', times)

        times = aggregate_bookmarks(db, random_seed=random_seed, test_count=test_count)
        log_aggregate_time(log_file, 'Get users bookmarks', times)

        log_file.write(f'finish time: ' + datetime.datetime.now().isoformat() + '\n')

    remove_test_collections(db)


if __name__ == '__main__':
    client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
    try:
        print(client.server_info())
    except Exception as exc:
        print("Unable to connect to the server.")
        raise exc

    db = client.speed_test
    measure_time(db, use_indexes=False)
    measure_time(db, use_indexes=True)
