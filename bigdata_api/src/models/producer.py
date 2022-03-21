import uuid
from datetime import datetime

from .base import BaseModel

from pydantic import StrictStr, validator


class ProducerMessage(BaseModel):
    created_at: StrictStr = ''
    user_id: uuid.UUID
    movie_id: uuid.UUID
    movie_time_offset: int

    @validator('created_at', pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')


class ProducerResponse(BaseModel):
    message: StrictStr
    status: StrictStr
