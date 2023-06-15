from rest_framework import pagination


class Pagination(pagination.PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        response = super(Pagination, self).get_paginated_response(data)
        response['count'] = self.page.paginator.count
        response['next'] = self.get_next_link()
        response['previous'] = self.get_previous_link()
        return response
