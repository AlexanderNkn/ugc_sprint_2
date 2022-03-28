import aiokafka
import backoff

producer: aiokafka.AIOKafkaProducer | None = None


async def get_producer() -> aiokafka.AIOKafkaProducer:
    return producer


class KafkaProducer:

    def __init__(self, kafka: aiokafka.AIOKafkaProducer):
        self.kafka = kafka

    @backoff.on_exception(backoff.expo, aiokafka.errors.KafkaError, max_time=120)
    async def send(self, topicname, msg, *args, **kwargs):
        return await self.kafka.send_and_wait(topicname, msg.encode('ascii'), *args, **kwargs)


class KafkaConsumer:

    def __init__(self, kafka: aiokafka.AIOKafkaConsumer):
        self.kafka = kafka

    @backoff.on_exception(backoff.expo, aiokafka.errors.KafkaError, max_time=120)
    async def consume(self):
        messages = []
        async for msg in self.kafka:
            messages.append(msg.value.decode())
        return messages
