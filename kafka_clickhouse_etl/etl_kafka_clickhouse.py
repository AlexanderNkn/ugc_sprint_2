from time import sleep

from clickhouse_driver import Client

from settings import CLICKHOUSE_HOST, CLICKHOUSE_PORT


def create_database(client: Client) -> None:
    client.execute(
        """
        CREATE DATABASE IF NOT EXISTS movies
        ON CLUSTER company_cluster
        """
    )
    sleep(60)


def create_source_tables(client: Client) -> None:
    """Fetch data from Kafka stream."""
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS movies.views_queue
        (
            user_id              UUID,
            movie_id             UUID,
            movie_time_offset    UInt64,
            created_at           DateTime
        )
        Engine=Kafka('broker:29092', 'views', 'views_group1', 'JSONEachRow')
        """
    )


def create_target_tables(client: Client) -> None:
    """Store data in ClickHouse."""
    client.execute(
        """
        CREATE TABLE IF NOT EXISTS movies.latest_view
        (
            user_id              UUID,
            movie_id             UUID,
            movie_time_offset    UInt64,
            created_at           DateTime
        )
        Engine=ReplacingMergeTree()
        ORDER BY (user_id, movie_id)
        """
    )

    client.execute(
        """
        CREATE TABLE IF NOT EXISTS movies.longest_view
        (
            user_id              UUID,
            movie_id             UUID,
            movie_time_offset    UInt64,
            created_at           DateTime
        )
        Engine=ReplacingMergeTree()
        ORDER BY (user_id, movie_id)
        """
    )


def create_materialized_view(client: Client) -> None:
    """Transfer data from Kafka to ClickHouse"""
    client.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS movies.latest_view_consumer
        TO movies.latest_view
        AS SELECT *
        FROM movies.views_queue
        """
    )

    client.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS movies.longest_view_consumer
        TO movies.longest_view
        AS SELECT *
        FROM movies.views_queue
        ORDER BY movie_time_offset
        """
    )


if __name__ == '__main__':
    client = Client(host=CLICKHOUSE_HOST, port=CLICKHOUSE_PORT)
    create_database(client)
    create_source_tables(client)
    create_target_tables(client)
    create_materialized_view(client)
