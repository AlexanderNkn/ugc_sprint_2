## Эндпойнты

### Отправка потоковых данных в Mongodb (через Kafka)

- лайк/дизлайк пользователя для фильма
    ```
    POST /movie-like
    {
        movie_id: uuid,
        user_id: uuid,
        like: bool
    }
    ```

- лайк/дизлайк пользователя для отзыва
    ```
    POST /review-like
    {
        rewiew_id: uuid,
        user_id: uuid,
        like: bool
    }
    ```

- отзыв пользователя для фильма
    ```
    POST /movie-rewiew
    {
        rewiew_id: uuid,
        movie_id: uuid,
        user_id: uuid,
        review: string
    }
    ```

- закладки пользователя
    ```
    POST /movie-bookmark
    {
        movie_id: uuid,
        user_id: uuid
    }
    ```

### Получение аггрегированных данных из Mongodb

- пользовательский контент к фильму(через сервис bigdata_api)
    ```
    GET /movie-ugc
    {
        movie_id: uuid,
        likes: integer,
        dislikes: integer,
        reviews: [
            {
                review_id: uuid,
                review: string,
                author_id: uuid,
                likes: integer,
                dislikes: integer
            },
            ...
        ]
    }
    ```

- закладки пользователя(через сервис bigdata_api)
    ```
    GET /movie-bookmarks
    {
        user_id: uuid,
        movies: [
            movie_id: uuid,
            ...
        ]
    }
    ```

- для получения данных напрямую из Mongodb подключитесь к контейнеру mongo
    ```
    docker-compose exec mongo1 mongo
    ```
- введите поисковый запрос
    ```
    rs0:PRIMARY> db.movie_ugc.find().pretty()

    {
            "_id" : ObjectId("62407ba358cde5cffb686e6e"),
            "movie_id" : "0fa418fb-e0c0-4175-9594-70f930fade78",
            "dislikes" : 1,
            "likes" : 3,
            "reviews" : [
                    {
                            "review_id" : "7b73b496-39da-4050-b4e0-38d946fd7e96",
                            "author_id" : "60f216f9-ed5f-4534-a425-c02101a5f4a1",
                            "review" : "11111",
                            "likes" : 2,
                            "dislikes" : 0
                    },
                    {
                            "review_id" : "ba9f92fc-ee7f-49d8-98b1-f1cd652ffeb4",
                            "author_id" : "7cbff603-14c4-4f7b-bc52-8a263db153f2",
                            "review" : "33333",
                            "likes" : 0,
                            "dislikes" : 2
                    }
            ]
    }
    {
            "_id" : ObjectId("62407ba358cde5cffb686e6f"),
            "movie_id" : "0680998d-b776-46db-a215-33370b32aa3c",
            "dislikes" : 2,
            "likes" : 2,
            "reviews" : [
                    {
                            "review_id" : "fb7b2c8e-ac9e-488c-b214-5548627dbdb1",
                            "author_id" : "60f216f9-ed5f-4534-a425-c02101a5f4a1",
                            "review" : "22222",
                            "likes" : 1,
                            "dislikes" : 1
                    },
                    {
                            "review_id" : "6d63cf94-c8ec-4d67-a518-c17d221b11cf",
                            "author_id" : "7cbff603-14c4-4f7b-bc52-8a263db153f2",
                            "review" : "44444"
                    }
            ]
    }
    ```