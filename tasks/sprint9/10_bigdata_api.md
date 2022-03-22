## Новые эндпойнты

Передавать и получать данные через Kafka Consumer и Producer

### Передача данных
Для передачи в Kafka данных о лайках к фильмам и отзывам, об отзывах к фильму и закладках пользователя добавить 5 эдпойнтов:
- /movie-likes
    {
        user_id: uuid,
        movie_id: uuid,
        like: bool or null
    }

- /movie-reviews
    {
        user_id: uuid,
        movie_id: uuid,
        review: text,
        review_id: uuid,  # добавляем поле при отправка данных из апи в кафку
        created_at: data  # добавляем поле при отправка данных из апи в кафку
    }

- /review-like
    {
        user_id: uuid,
        review_id: uuid,
        like: bool or null
    }

- /add-movie-bookmark
    {
        user_id: uuid,
        movie_id: uuid
    }

- /delete-movie-bookmark
    {
        user_id: uuid,
        movie_id: uuid
    }


### Получение данных
Для получения данных из Kafka 2 эдпойнтa:
- /get-movie-ugc
    {
        movie_id: uuid,
        like: int,
        dislike: int,
        rating  # не храним в Mongo, высчитываем в bigdata_api как (like * 10) / (like + dislike)
        review_id: [
            author_id: int
            created_at: date,
            like: int,
            dislike: int
        ]
    }

- /get-bookmarks
    {
        user_id: uuid,
        bookmarks: [
            movie_id: uuid
        ]
    }

Подзадачи:
- 11_bigdata_docs
- 12_bigdata_tests

Оценка 5
