from rest_framework.pagination import PageNumberPagination


class BaseViewPagination(PageNumberPagination):
    page_size = 10


class BaseApiPagination(PageNumberPagination):
    page_size = 10


class BaseAdminPagination:
    list_per_page = 20
