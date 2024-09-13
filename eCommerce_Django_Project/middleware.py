import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from customer.logged_pages import check_login


class CustomMiddleWare:

    def is_decorated(self, func):
        return hasattr(func, "__closure__") and any(
            c.cell_contents == check_login for c in func.__closure__
        )

    def __init__(self, get_response):
        self.get_response = get_response
        self.a = 0

    def __call__(self, request):

        self.a += 1
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        # Log the request details
        request_time = end_time - start_time
        view_function = None
        if hasattr(request, "resolver_match") and request.resolver_match is not None:
            view_function = request.resolver_match.func.__name__
        method = request.method
        path = request.path_info
        status_code = response.status_code

        log_message = f"Method: {method}, Path: {path}, View function: {view_function}, Status code: {status_code}, Time taken: {request_time:.6f} seconds"
        logger.info(log_message)

        return response
