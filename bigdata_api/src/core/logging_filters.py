import logging

from fastapi import Header


class RequestIdFilter(logging.Filter):
    def filter(self, record, x_request_id=Header(None)):
        record.request_id = x_request_id
        return True
