from db.abstract_storage import AbstractProducer


class MessageProducer(AbstractProducer):

    async def send(self, topicname, msg, *args, **kwargs):
        return await self.engine.send(topicname=topicname, msg=msg.json(), *args, **kwargs)


class MessageConsumer(AbstractProducer):

    async def send(self, *args, **kwargs):
        return await self.engine.consume(*args, **kwargs)
