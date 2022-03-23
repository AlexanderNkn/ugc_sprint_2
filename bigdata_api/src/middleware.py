import sentry_sdk
from starlette.middleware.base import BaseHTTPMiddleware


class SentryErrorLogging(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_context("request", request)
                scope.user = {
                    "ip_address": request.client.host,
                }
                sentry_sdk.capture_exception(e)
            raise e
