from rest_framework.pagination import PageNumberPagination


class StudioPagination(PageNumberPagination):
    page_size = 10  # 기본 페이지당 항목 수
    page_size_query_param = "page_size"
    max_page_size = 100  # 최대 페이지당 항목
