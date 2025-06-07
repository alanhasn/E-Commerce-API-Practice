# Custom pagination class for API responses
from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination



class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_query_param = 'page_num'  # Query parameter for the page number
    page_size_query_param = 'page_size'  # Query parameter for the page size
    max_page_size = 100  # Maximum page size a  llowed


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # Default limit for the number of items per page
    limit_query_param = 'per_page'  # Query parameter for the limit
    offset_query_param = 'start'  # Query parameter for the offset
    max_limit = 100  # Maximum limit allowed
    
# This pagination class can be used to implement cursor-based pagination if needed.
class CustomCursorPagination(LimitOffsetPagination):
    """
    Custom cursor pagination class that extends LimitOffsetPagination.
    This class can be used to implement cursor-based pagination if needed.
    """
    ordering = 'order_id'
    page_size = 10