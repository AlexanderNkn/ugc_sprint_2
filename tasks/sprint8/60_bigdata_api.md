## Сервис bigdata. Эндпойнт

Написать сервис bigdata_api для отправки данных в bigdata_etl.

Фреймворк - fastapi
Авторизация через сервис auth
Эндпойнт принимает post запрос, содержащий user_id, movie_id и временную метку просматриемого фильма. Затем пересылает эти данные в Kafka(bigdata_etl)

Подзадачи:
- 61_bigdata_docs
- 62_bigdata_tests

Оценка 8