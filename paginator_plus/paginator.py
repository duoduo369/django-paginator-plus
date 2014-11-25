# -*- coding: utf-8 -*-
from django.core.paginator import Paginator as DjangoPaginator, Page as DjangoPage
from copy import copy
import math


class PaginatorMixin(object):
    '''
    PaginatorMixin, Mixin to DjangoPaginator, subclass need attr page_num.
    '''

    def __init__(self, display_pages=10, curr_page=1, **kwargs):
        self.display_pages = display_pages
        self.curr_page = curr_page


class RequestPaginatorMixin(PaginatorMixin):
    def __init__(self, first_text = u'first', last_text = u'last',
                show_first = True, show_last = True,
                show_prev = True, show_next = True,
                prev_page_text = u'prev page', next_page_text = u'next page',
                auto_hide_prev = True, auto_hide_next = True,
                *args, **kwargs):
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
        super(RequestPaginatorMixin, self).__init__(*args, **kwargs)


class Paginator(DjangoPaginator, PaginatorMixin):
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        PaginatorMixin.__init__(self, **kwargs)
        DjangoPaginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)

    @property
    def page_range(self):
        '''
        if you display_pages = 10, curr_page = 10
        page_range will be [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        '''
        start = max(1, self.curr_page - int(math.ceil(self.display_pages / 2)))
        end = start + self.display_pages - 1
        if end > self.num_pages:
            end = self.num_pages
            start = max(1, self.num_pages - self.display_pages)
        return range(start, end+1)
