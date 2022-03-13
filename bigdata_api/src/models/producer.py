import uuid
from datetime import datetime

from .base import BaseModel

from pydantic import StrictStr, validator


class ProducerMessage(BaseModel):
    message_id: StrictStr = ""
    timestamp: StrictStr = ""
    user_id: uuid.UUID
    movie_id: uuid.UUID
    movie_time_offset: int

    @validator("message_id", pre=True, always=True)
    def set_id_from_uuid(cls, v):
        return str(uuid.uuid4())

    @validator("timestamp", pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return str(datetime.utcnow())


class ProducerResponse(BaseModel):
    message_id: StrictStr
    topic: StrictStr
    timestamp: StrictStr = ""

    @validator("timestamp", pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return str(datetime.utcnow())
