from dependencies.authentication import get_token, make_request
from fastapi import APIRouter, Depends, Header, status

from models.producer import ProducerMessage, ProducerResponse
from services.producer import ProducerService, get_producer_service

router = APIRouter()


async def check_views_statistics_permission(token=get_token(), x_request_id=Header(None)):
    await make_request(permission='views_statistic', token=token, x_request_id=x_request_id)


# TODO in current implementation different topics will be validated by pydantic with
# the same fields, hardcoded in ProducerMessage model. Custom router should be added to map
# topicname with its model before processing with kafka_produce() callable. This approach
# will allow to reuse this endpoint for different topicname-model combinations.
@router.post(
    '/{topicname}',
    status_code=status.HTTP_201_CREATED,
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
    return ProducerResponse(
        status='success',
        message='acknowledged',
    )
