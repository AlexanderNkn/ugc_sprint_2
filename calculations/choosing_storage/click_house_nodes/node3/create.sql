CREATE DATABASE shard;
CREATE DATABASE replica;

CREATE TABLE shard.test
(
    user_id      Int64,
    movie_id     String,
    viewed_frame Int64
)
    Engine = ReplicatedMergeTree('/clickhouse/tables/shard1/test', 'replica_1') ORDER BY user_id;

CREATE TABLE replica.test
(
    user_id      Int64,
    movie_id     String,
    viewed_frame Int64
)
    Engine = ReplicatedMergeTree('/clickhouse/tables/shard2/test', 'replica_2') ORDER BY user_id;


CREATE TABLE default.test
(
    user_id      Int64,
    movie_id     String,
    viewed_frame Int64
)
    ENGINE = Distributed('company_cluster', '', test, rand());