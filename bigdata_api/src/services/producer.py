from functools import lru_cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from db.kafka_db import KafkaProducer, get_producer
from db.storage import MessageProducer
from models.producer import ProducerMessage, ProducerResponse


class ProducerService:

    def __init__(self, producer: MessageProducer) -> None:
        self.producer = producer

    async def send(self, topicname: str, msg: ProducerMessage) -> ProducerResponse | None:
        return await self.producer.send(topicname, msg)


@lru_cache()
def get_producer_service(
    kafka: AIOKafkaProducer = Depends(get_producer)
) -> ProducerService:
    producer: MessageProducer = MessageProducer(KafkaProducer(kafka))
    return ProducerService(producer=producer)
