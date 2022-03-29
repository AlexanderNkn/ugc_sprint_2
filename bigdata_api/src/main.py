import logging

import aiokafka
import backoff
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import producer
from core import config
from core.logger import LOGGING
from db import kafka_db


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/bigdata-api/openapi',
    redoc_url='/bigdata-api/redoc',
    openapi_url='/bigdata-api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Collect information about movies views',
    version='1.0.0'
)


@app.on_event('startup')
@backoff.on_exception(backoff.expo, aiokafka.errors.KafkaError, max_time=120)
async def startup():
    kafka_db.producer = aiokafka.AIOKafkaProducer(
        client_id=config.PROJECT_NAME, bootstrap_servers=config.KAFKA_INSTANCE
    )
    await kafka_db.producer.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka_db.producer.stop()


app.include_router(producer.router, prefix='/bigdata-api/v1/producer', tags=['producer'])


if __name__ == '__main__':

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=config.BIGDATASPI_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
