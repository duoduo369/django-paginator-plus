# -*- coding: utf-8 -*-
import math
from copy import copy
from urllib import urlencode
from django.core.paginator import Paginator as DjangoPaginator


class PaginatorMixin(object):
    '''
    PaginatorMixin, Mixin to DjangoPaginator, subclass need attr page_num.
    '''

    def __init__(self, display_pages=10, curr_page=1, **kwargs):
        display_pages = int(display_pages)
        curr_page = int(curr_page)
        self.display_pages = display_pages
        self.curr_page = curr_page


class RequestPaginatorMixin(PaginatorMixin):
    def __init__(self, request=None, page_num_param=u'page',
                 show_prev=True, show_next=True,
                 prev_page_text=u'Previous', next_page_text=u'Next',
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
            paginator.curr_page = 1
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
        return paginator_page_range(self)

    @property
    def page_params_range(self):
        '''
         from left to right might be

             Previous 1 ... 2 3 4 5 ... 3000 Next
             Previous 1 2 3 4 5 ... 3000 Next
             1 2 3 4 5 ... 3000 Next
        all depand on you

        '''
        def get_page_url(_params, page_num):
            _params[self.page_num_param] = page_num
            return '{}?{}'.format(self.url_path, urlencode(_params))

        def get_page_meta_dict(text, url_params, clickable=True, current=False):
            return {
                'clickable': clickable,
                'current': current,
                'text': text,
                'url_params': url_params
            }

        _page_range = self.page_range
        page_rage = []
        params = copy(self.get_params)
        if self.show_prev:
            if self.curr_page == 1:
                # in first page
                if not self.auto_hide_prev:
                    page_rage.append(get_page_meta_dict(self.prev_page_text, get_page_url(params, 1), clickable=False))
            else:
                page_rage.append(get_page_meta_dict(self.prev_page_text, get_page_url(params, self.curr_page-1)))

        if _page_range[0] != 1:
            page_rage.append(get_page_meta_dict(1, get_page_url(params, 1)))
            page_rage.append(get_page_meta_dict('...', '', clickable=False))

        for pr in _page_range:
            meta_dict = get_page_meta_dict(pr, get_page_url(params, pr))
            if pr == self.curr_page:
                meta_dict['current'] = True
                meta_dict['clickable'] = False
            page_rage.append(meta_dict)

        if _page_range[len(_page_range)-1] < self.num_pages:
            page_rage.append(get_page_meta_dict('...', '', clickable=False))
            page_rage.append(get_page_meta_dict(self.num_pages, get_page_url(params, self.num_pages)))

        if self.show_next:
            if self.curr_page >= self.num_pages:
                if not self.auto_hide_next:
                    page_rage.append(get_page_meta_dict(self.next_page_text, get_page_url(params, self.num_pages), clickable=False))
            else:
                page_rage.append(get_page_meta_dict(self.next_page_text, get_page_url(params, self.curr_page+1)))

        return page_rage

    @property
    def page(self):
        return super(RequestPaginator, self).page(self.curr_page)
