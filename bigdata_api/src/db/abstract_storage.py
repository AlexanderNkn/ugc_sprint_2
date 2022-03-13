from abc import ABC, abstractmethod


class AbstractProducer(ABC):
    """Abstract class for message producer."""

    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    async def send(self, *args, **kwargs):
        pass


class AbstractConsumer(ABC):
    """Abstract class for message consumer."""

    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    async def consume(self, *args, **kwargs):
        pass
