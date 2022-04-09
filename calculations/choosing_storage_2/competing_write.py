import asyncio
import os
import sys

import pymongo

import logging
from logging import config

from logging_config import LOGGING_CONFIG
from settings import MONGO_HOST, MONGO_PORT

import work_with_data
import mongodb

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('choosing_storage_mongo')


async def generate_movie_likes(db, random_seed=None, bulk_size=10_000, samples=10_000_000) -> None:
    return mongodb.generate_movie_likes(db, random_seed, bulk_size, samples)


async def generate_movie_reviews(db, random_seed=None, bulk_size=10_000, samples=5_000_000) -> None:
    return mongodb.generate_movie_reviews(db, random_seed, bulk_size, samples)


async def generate_movie_bookmarks(db, random_seed=None, bulk_size=10_000, max_bookmarks=20) -> None:
    return mongodb.generate_movie_bookmarks(db, random_seed, bulk_size, max_bookmarks)


async def aggregate_test(db, random_seed=42, test_count=10):
    times = mongodb.aggregate_movies_likes(db, random_seed=random_seed, test_count=test_count)
    mongodb.log_aggregate_time(sys.stdout, 'Get movies ranking', times)

    times = mongodb.aggregate_user_likes(db, random_seed=random_seed, test_count=test_count)
    mongodb.log_aggregate_time(sys.stdout, 'Get users likes', times)

    times = mongodb.aggregate_bookmarks(db, random_seed=random_seed, test_count=test_count)
    mongodb.log_aggregate_time(sys.stdout, 'Get users bookmarks', times)


def measure_time(db):

    result_dir = os.path.join(work_with_data.ROOT_DIR, 'results')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir, exist_ok=True)

    mongodb.remove_test_collections(db)
    mongodb.prepare_collections(db, use_indexes=True)

    random_seed = 42

    bulk_size = 10_000
    movie_likes_samples = 10_000_000
    movie_reviews_samples = 5_000_000
    users_max_bookmarks = 20

    test_count = 100

    users = work_with_data.read_users(work_with_data.ROOT_DIR)
    movies = work_with_data.read_movies(work_with_data.ROOT_DIR)
    reviews = work_with_data.read_reviews(work_with_data.ROOT_DIR)

    print(f'Users count: {len(users)}\n')
    print(f'Movies count: {len(movies)}\n')
    print(f'Reviews count: {len(reviews)}\n')
    print('\n')

    users = work_with_data.read_users(work_with_data.ROOT_DIR)
    movies = work_with_data.read_movies(work_with_data.ROOT_DIR)
    reviews = work_with_data.read_reviews(work_with_data.ROOT_DIR)

    print(f'Users count: {len(users)}\n')
    print(f'Movies count: {len(movies)}\n')
    print(f'Reviews count: {len(reviews)}\n')
    print('\n')

    print(f'bulk_size: {bulk_size}\n')
    print(f'users max_bookmarks: {users_max_bookmarks}\n')

    print(f'movie_likes samples: {movie_likes_samples}\n')
    print(f'movie_reviews samples: {movie_reviews_samples}\n')
    print('\n')

    # сначала заполним частью данных
    # ioloop = asyncio.get_event_loop()
    ioloop = asyncio.new_event_loop()
    asyncio.set_event_loop(ioloop)
    tasks = [
        ioloop.create_task(generate_movie_likes(db, random_seed=random_seed,
                                                bulk_size=bulk_size, samples=movie_likes_samples)),
        ioloop.create_task(generate_movie_reviews(db, random_seed=random_seed,
                                                  bulk_size=bulk_size, samples=movie_reviews_samples)),
        ioloop.create_task(generate_movie_bookmarks(db, random_seed=random_seed,
                                                    bulk_size=bulk_size, max_bookmarks=users_max_bookmarks)),
    ]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    # ioloop.close()

    print('\nTime for aggregate operation (ms):\n\n')

    # times = mongodb.aggregate_movies_likes(db, random_seed=random_seed, test_count=test_count)
    # mongodb.log_aggregate_time(sys.stdout, 'Get movies ranking', times)
    #
    # times = mongodb.aggregate_user_likes(db, random_seed=random_seed, test_count=test_count)
    # mongodb.log_aggregate_time(sys.stdout, 'Get users likes', times)
    #
    # times = mongodb.aggregate_bookmarks(db, random_seed=random_seed, test_count=test_count)
    # mongodb.log_aggregate_time(sys.stdout, 'Get users bookmarks', times)

    # ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(generate_movie_likes(db, random_seed, bulk_size=5, samples=movie_likes_samples//10)),
        ioloop.create_task(generate_movie_reviews(db, random_seed, bulk_size=5, samples=movie_reviews_samples//10)),
        ioloop.create_task(generate_movie_bookmarks(db, random_seed, bulk_size=5, max_bookmarks=users_max_bookmarks)),
        aggregate_test(db, random_seed, test_count=test_count),
    ]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()


if __name__ == '__main__':
    client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
    try:
        print(client.server_info())
    except Exception as exc:
        print("Unable to connect to the server.")
        raise exc

    db = client.speed_test
    measure_time(db)
