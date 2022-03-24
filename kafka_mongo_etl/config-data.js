db = db.getSiblingDB('user_content');
db.createCollection('movie_likes');
db.createCollection('reviews');
db.createCollection('review_likes');
db.createCollection('bookmarks');
db.createCollection('movie_ugc');
