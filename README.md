# Проектная работа 8 спринта
Задачи можно посмотреть в /tasks

## Ссылка на репозиторий с проектом:
https://github.com/AlexanderNkn/ugc_sprint_1

## Выбор аналитической базы данных
Сравнивали Vertica и ClickHouse. На нашем наборе данных ClickHouse показала лучшие результаты

Записано 55000 записей в Vetrica за 1.0577869415283203 
Прочитано 55000 записей в Vetrica за 0.9722421169281006 
Записано 55000 записей в ClickHouse за 0.23347997665405273 
Прочитано 55000 записей в ClickHouse за 0.07249212265014648

Скрипты находятся в calculations/choosing_storage
Описание запуска проекта в [readme](calculations/choosing_storage/README.md)
