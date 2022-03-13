# Проектная работа 8 спринта
Задачи можно посмотреть в /tasks

## Ссылка на репозиторий с проектом:
https://github.com/AlexanderNkn/ugc_sprint_1

## Описание
Это API для для сохранения информации о просматриваемом пользователем фильме. Данные сохраняются потоком в событийную базу данных Kafka, а из нее в фоне ETL-процессом перекладываются в аналитическую базу ClickHouse.

## Установка
- склонируйте проект с реппозитория GitHub
    ```
    git clone https://github.com/AlexanderNkn/ugc_sprint_1.git
    ```
- переименуйте файл с переменными окружения для тестирования
    ```
    mv bigdata_api/envs/.bigdata_api.env.sample bigdata_api/envs/.bigdata_api.env
    ```
- соберите образ
    ```
    docker-compose build --no-cache
    ```
- запустите проект
    ```
    docker-compose up -d
    ```

## Документация 
- Доступна по адресу
    ```
    http://localhost/bigdata-api/openapi
    ```
- В json формате
    ```
    http://localhost/bigdata-api/openapi.json
    ```

## Использование
### отправка данных в Kafka
- 
    ```
    localhost/bigdata-api/v1/producer/views
    
    curl --location --request POST 'localhost/bigdata-api/v1/producer/views' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "user_id": "46a5143b-9fbe-4483-a9be-30ebccf7132c",
        "movie_id": "46a5143b-9fbe-4483-a9be-30ebccf7132c",
        "movie_time_offset": 124000,
        "created_at": "2022-02-03 12:03:05"
    }'

    201 Created

    {
        "message": "acknowledge",
        "status": "success"
    }
    ```

### получение последней временной метки для конкретного пользователя и фильма

- Для просмотра данных, переданных в ClickHouse подключитесь к первой ноде
    ```
    docker-compose exec clickhouse-node1 clickhouse-client 
    ```

- пример запроса для получения метки последнего просмотра выбранного конкретного пользователя и фильма
    ```
    clickhouse-node1 :) SELECT * FROM movies.latest_view FINAL;
    
    SELECT *
    FROM movies.latest_view
    FINAL
    
    Query id: 6fa40801-f0f4-4198-b64d-aea4ea5bdb04
    
    ┌─user_id──────────────────────────────┬─movie_id─────────────────────────────┬─movie_time_offset─┬──────────created_at─┐
    │ 46a5143b-9fbe-4483-a9be-30ebccf7132c │ 46a5143b-9fbe-4483-a9be-30ebccf7132c │            124000 │ 2022-02-03 12:03:05 │
    └──────────────────────────────────────┴──────────────────────────────────────┴───────────────────┴─────────────────────┘
    
    1 rows in set. Elapsed: 0.003 sec.
    ```
