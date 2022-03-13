from fastapi import APIRouter, Depends, Header

from dependencies.authentication import get_token, make_request
from models.producer import ProducerMessage, ProducerResponse
from services.producer import ProducerService, get_producer_service

router = APIRouter()


async def check_views_statistics_permission(token=get_token(), x_request_id=Header(None)):
    await make_request(permission='views_statistic', token=token, x_request_id=x_request_id)


@router.post(
    '/{topicname}',
    response_model=ProducerResponse,
    summary='Send message to kafka',
    description='Send message to kafka',
    response_description='Topic name and message id',
)
async def kafka_produce(
    msg: ProducerMessage,
    topicname: str,
    producer_service: ProducerService = Depends(get_producer_service),
    allowed: bool = Depends(check_views_statistics_permission),
) -> ProducerResponse:
    await producer_service.send(topicname, msg)
    response = ProducerResponse(
        message_id=msg.message_id, topic=topicname
    )

    return response
