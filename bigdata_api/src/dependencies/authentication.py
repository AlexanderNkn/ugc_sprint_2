import aiohttp
import pybreaker
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='', auto_error=config.ENABLE_AUTHORIZATION)
db_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)


def get_token(token: str = Depends(oauth2_scheme)):
    return token


# db_breaker is an implementation of Circuit Breaker algorithm
@db_breaker(__pybreaker_call_async=True)
async def make_request(permission: str, token: str, x_request_id: str):
    if not config.ENABLE_AUTHORIZATION:
        return
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f'{config.AUTH_HOST}:{config.AUTH_PORT}{config.AUTH_BASE_URL}/check-permission',
            json={'permission': f'{permission}'},
            headers={
                'Authorization': f'Bearer {token}',
                'X-Request-Id': x_request_id,
            },
        ) as response:
            authentication_data = await response.json()
            if authentication_data['status'] == 'error' or (
                authentication_data['status'] == 'success' and authentication_data['has_permission'] is False
            ):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=authentication_data)
