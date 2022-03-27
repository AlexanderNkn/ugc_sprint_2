db = db.getSiblingDB('user_content');

db.createCollection('movie_likes');
db.movie_likes.createIndex({'user_id': 1, 'movie_id': 1}, { unique: true });

db.createCollection('reviews');
db.reviews.createIndex({'review_id': 1}, { unique: true });

db.createCollection('review_likes');
db.review_likes.createIndex({'user_id': 1, 'review_id': 1}, { unique: true });

db.createCollection('bookmarks');
db.bookmarks.createIndex({'user_id': 1, 'movie_id': 1}, { unique: true });

db.createCollection('movie_ugc');
db.movie_ugc.createIndex({'movie_id': 1}, { unique: true });
