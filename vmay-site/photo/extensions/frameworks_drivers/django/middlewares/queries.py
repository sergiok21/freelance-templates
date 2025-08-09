from loguru import logger

from django.db import connection, reset_queries


class QueryCountDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reset_queries()
        response = self.get_response(request)
        num_queries = len(connection.queries)
        logger.debug(f'SQL queries: {num_queries}')
        return response
