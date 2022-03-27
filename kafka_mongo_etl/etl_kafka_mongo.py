import logging
from logging import config
from time import sleep

from pymongo import MongoClient

from logging_config import LOGGING_CONFIG
from settings import MONGO_HOST, MONGO_PORT

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('etl_kafka_mongo')


def aggregate_review_likes(db) -> None:
    db.review_likes.aggregate([
        {
            "$group": {
                "_id": {
                    "review_id": "$review_id"
                },
                "likes": {
                    "$sum": {
                        "$cond": {"if": {"$eq": ["$like", True]}, "then": 1, "else": 0 }
                    }
                },
                "dislikes": {
                    "$sum": {
                        "$cond": {"if": {"$eq": ["$like", False]}, "then": 1, "else": 0 }
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "review_id": "$_id.review_id",
                "likes": 1,
                "dislikes": 1
            }
        },
        {
            "$merge": {
                "into": "reviews",
                "on": "review_id",
                "whenMatched": "merge",
                "whenNotMatched": "insert"
            }
        }
    ])


def aggregate_movie_likes(db) -> None:
    db.movie_likes.aggregate([
        {
            "$group": {
                "_id": {
                    "movie_id": "$movie_id"
                },
                "likes": {
                    "$sum": {
                        "$cond": {"if": {"$eq": ["$like", True]}, "then": 1, "else": 0 }
                    }
                },
                "dislikes": {
                    "$sum": {
                        "$cond": {"if": {"$eq": ["$like", False]}, "then": 1, "else": 0 }
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "movie_id": "$_id.movie_id",
                "likes": 1,
                "dislikes": 1
            }
        },
        {
            "$merge": {
                "into": "movie_ugc",
                "on": "movie_id",
                "whenMatched": "merge",
                "whenNotMatched": "insert"
            }
        }
    ])


def aggregate_movie_ugc_data(db) -> None:
    db.reviews.aggregate([
        {
            "$group": {
                "_id": {
                    "movie_id": "$movie_id"
                },
                "reviews": {
                    "$push": {
                        "review_id": "$review_id",
                        "author_id": "$user_id",
                        "review": "$review",
                        "likes": "$likes",
                        "dislikes": "$dislikes"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "movie_id": "$_id.movie_id",
                "reviews": 1
            }
        },
        {
            "$merge": {
                "into": "movie_ugc",
                "on": "movie_id",
                "whenMatched": "merge",
                "whenNotMatched": "insert"
            }
        }
    ])


if __name__ == '__main__':
    client = MongoClient(f'mongodb://{MONGO_HOST}:{MONGO_PORT}')
    db = client.user_content
    while True:
        try:
            aggregate_review_likes(db)
            aggregate_movie_likes(db)
            aggregate_movie_ugc_data(db)
        except:
            logger.exception('Something went wrong with Mongodb')
        # TODO add circuit breaker
        sleep(60)
