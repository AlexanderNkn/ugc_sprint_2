## Описание
Это ETL для перегрузки данных из Kafka в ClickHouse

## Установка
- соберите образ
    ```
    docker-compose build --no-cache
    ```
- запустите проект
    ```
    docker-compose up -d
    ```

## Использование
- Для просмотра данных, переданных в ClickHouse подключитесь к первой ноде
    ```
    docker-compose exec clickhouse-node1 clickhouse-client 
    ```

- пример запроса для получения метки последнего просмотра выбранного конкретного пользователя и фильма
    ```
    clickhouse-node1 :) SELECT * FROM movies.latest_view FINAL
    
    SELECT *
    FROM movies.latest_view
    FINAL
    
    Query id: 33cf5cf9-4124-44dc-8202-76195457ebac
    
    ┌─user_id──────────────────────────────┬─movie_id─────────────────────────────┬─movie_time_offset─┬──────────created_at─┐
    │ 46a5143b-9fbe-4483-a9be-30ebccf7132c │ 46a5143b-9fbe-4483-a9be-30ebccf7132c │            123000 │ 2022-03-13 20:17:36 │
    └──────────────────────────────────────┴──────────────────────────────────────┴───────────────────┴─────────────────────┘
    
    1 rows in set. Elapsed: 0.003 sec. 
    ```
