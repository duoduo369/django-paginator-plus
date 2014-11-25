# -*- coding: utf-8 -*-
import math
from copy import copy
from urllib import urlencode

from django.core.paginator import Page as DjangoPage
from django.core.paginator import Paginator as DjangoPaginator
from django.core.paginator import EmptyPage


class PaginatorMixin(object):
    '''
    PaginatorMixin, Mixin to DjangoPaginator, subclass need attr page_num.
    '''

    def __init__(self, display_pages=10, curr_page=1, **kwargs):
        self.display_pages = display_pages
        self.curr_page = curr_page


class RequestPaginatorMixin(PaginatorMixin):
    def __init__(self, request=None, page_num_param=u'page',
                first_text=u'first', last_text=u'last',
                show_first=True, show_last=True,
                show_prev=True, show_next=True,
                prev_page_text=u'prev page', next_page_text=u'next page',
                auto_hide_prev=True, auto_hide_next=True,
                url_path='',
                *args, **kwargs):
        assert request, 'request must not be None'
        self._request = request
        if not url_path:
            url_path = request.path_info
        self.url_path = url_path
        self.get_params = request.GET.dict()
        self.page_num_param = page_num_param
        self.first_text = first_text
        self.last_text = last_text
        self.show_first = show_first
        self.show_last = show_last
        self.show_prev = show_prev
        self.show_next = show_next
        self.prev_page_text = prev_page_text
        self.next_page_text = next_page_text
        self.auto_hide_prev = auto_hide_prev
        self.auto_hide_next = auto_hide_next
        if 'curr_page' not in kwargs:
            curr_page = self.get_params.get(page_num_param)
            if curr_page:
                kwargs['curr_page'] = curr_page

        super(RequestPaginatorMixin, self).__init__(*args, **kwargs)


def validate_number_patch(paginator, curr_page):
    if curr_page < 1:
        if paginator.allow_empty_first_page:
            p.curr_page = 1
    if curr_page > paginator.num_pages:
       paginator.curr_page = paginator.num_pages


def paginator_page_range(paginator):
    '''
    if you display_pages = 10, curr_page = 10
    page_range will be [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    '''
    start = max(1, paginator.curr_page - int(math.ceil(paginator.display_pages / 2)))
    end = start + paginator.display_pages - 1
    if end > paginator.num_pages:
        end = paginator.num_pages
        start = max(1, paginator.num_pages - paginator.display_pages + 1)
    return range(start, end+1)


class Paginator(DjangoPaginator, PaginatorMixin):

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        PaginatorMixin.__init__(self, **kwargs)
        DjangoPaginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        validate_number_patch(self, self.curr_page)

    @property
    def page_range(self):
        return paginator_page_range(self)

    @property
    def page(self):
        validate_number_patch(self, self.curr_page)
        return super(Paginator, self).page(self.curr_page)


class RequestPaginator(DjangoPaginator, RequestPaginatorMixin):

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        RequestPaginatorMixin.__init__(self, **kwargs)
        DjangoPaginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        validate_number_patch(self, self.curr_page)

    @property
    def page_range(self):
        '''
        if you display_pages = 10, curr_page = 10
        page_range will be [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        '''
        _range = paginator_page_range(self)
        _page_range = []
        _params = copy(self.get_params)
        for i in _range:
            _params[self.page_num_param] = i
            _page_range.append('{}?{}'.format(self.url_path, urlencode(_params)))
        return _page_range

    @property
    def page(self):
        return super(RequestPaginator, self).page(self.curr_page)
