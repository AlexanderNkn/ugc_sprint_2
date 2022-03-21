### Тестирование Баз данных 


1. Запустите компоуз файл для поднятия Clickhouse и Vetrica
```
docker-compose up --build 
```

2. Настройка Clickhouse:

- Перейдите в контейнеры 
``` 
docker exec -it clickhouse-node3 bash 
docker exec -it clickhouse-node1 bash 
```

- И в каждом выполните команду для создания таблицы и базы данных
``` 
clickhouse-client --multiquery < /etc/clickhouse-server/create.sql
``` 

3. Выполните команду pip -r install requirements.txt
4. Запускайте **main.py** 
5. Результаты вставки и чтения 10_000 записей будут в файле **results.txt**

