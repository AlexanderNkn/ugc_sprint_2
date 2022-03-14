import json

from fastapi.testclient import TestClient

from bigdata_api.src.main import app

client = TestClient(app)


def test_kafka_producer_payload(mocker):
    mocker.patch('bigdata_api.src.api.v1.producer.ProducerService.send', return_value=True)
    response = client.post(
        '/bigdata-api/v1/producer/views',
        json={
            "user_id": "",
            "movie_id": "46a5143b-9fbe-4483-a9be-30ebccf7132c",
            "movie_time_offset": 124000,
            "created_at": "2022-02-03 12:03:05"
        }
    )

    assert response.status_code == 422, 'check request body'


def test_kafka_producer_response(mocker):
    mocker.patch('bigdata_api.src.api.v1.producer.ProducerService.send', return_value=True)
    response = client.post(
        '/bigdata-api/v1/producer/views',
        json={
            "user_id": "46a5143b-9fbe-4483-a9be-30ebccf7132c",
            "movie_id": "46a5143b-9fbe-4483-a9be-30ebccf7132c",
            "movie_time_offset": 124000,
            "created_at": "2022-02-03 12:03:05"
        }
    )

    assert response.status_code == 201
    producer_message_expected = {
        "message": "acknowledged",
        "status": "success"
    }
    assert json.loads(response.content) == producer_message_expected
