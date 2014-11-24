# -*- coding: utf-8 -*-
from django.core.paginator import Paginator as DjangoPaginator, Page as DjangoPage
from copy import copy
import math


class PaginatorMixin(object):
    '''
    PaginatorMixin, Mixin to DjangoPaginator, subclass need attr page_num.
    '''
    FIRST_TEXT = u'first'
    LAST_TEXT = u'last'
    SHOW_FIRST = True
    SHOW_LAST = True
    DISPLAY_PAGES = 10
    PREV_PAGE_TEXT = u'prev page'
    NEXT_PAGE_TEXT = u'next page'

    def __init__(self, *args, **kwargs):
        self.page_num

    @property
    def TOTAL_COUNT(self):
        return self.count

    @property
    def MAX_PAGE_NUM(self):
        return self.num_pages

    @property
    def PAGE_RANGE(self):
        start = max(1, self.page_num - int(math.ceil(self.DISPLAY_PAGES / 2)))
        end = start + self.DISPLAY_PAGES - 1
        if end > self.MAX_PAGE_NUM:
            end = self.MAX_PAGE_NUM
            start = max(1, self.MAX_PAGE_NUM - self.DISPLAY_PAGES)
        return range(start, end+1)


class Paginator(DjangoPaginator, PaginatorMixin):
    def __init__(self, object_list, per_page, page_num, orphans=0,
                 allow_empty_first_page=True, **extra_data):
        self.page_num = page_num
        self.extra_data = copy(extra_data)
        super(Paginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

class Page(DjangoPage):
    pass
