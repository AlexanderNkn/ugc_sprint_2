from fastapi import APIRouter, Depends

# from dependencies.authentication import get_token, make_request
from models.producer import ProducerMessage, ProducerResponse
from services.producer import ProducerService, get_producer_service

router = APIRouter()


@router.post(
    '/{topicname}',
    response_model=ProducerResponse,
    summary='Send massage to kafka',
    description='Send massage to kafka',
    response_description='Topicname and message id',
)
async def kafka_produce(msg: ProducerMessage, topicname: str,
                        producer_service: ProducerService = Depends(get_producer_service),
                        ):
    await producer_service.send(topicname, msg)
    response = ProducerResponse(
        message_id=msg.message_id, topic=topicname
    )

    return response
