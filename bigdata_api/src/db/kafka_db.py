import aiokafka.errors
import backoff
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

producer: AIOKafkaProducer | None = None


async def get_producer() -> AIOKafkaProducer:
    return producer


class KafkaProducer:

    def __init__(self, kafka: AIOKafkaProducer):
        self.kafka = kafka

    @backoff.on_exception(backoff.expo, aiokafka.errors.KafkaError, max_time=120)
    async def send(self, topicname, msg, *args, **kwargs):
        return await self.kafka.send_and_wait(topicname, msg.encode("ascii"), *args, **kwargs)


class KafkaConsumer:

    def __init__(self, kafka: AIOKafkaConsumer):
        self.kafka = kafka

    @backoff.on_exception(backoff.expo, aiokafka.errors.KafkaError, max_time=120)
    async def consume(self):
        async for msg in self.kafka:
            return msg.value.decode()
