django-paginator-plus
===

Want to save the url params and get a format page_range?

This package save extra data to django paginator. Useful when url has params.

If you want to get page rang like below, then Use RequestPaginator.

    Previous 1 ... 2 3 4 5 ... 3000 Next
    Previous 1 2 3 4 5 ... 3000 Next
    1 2 3 4 5 ... 3000 Next

RequestPaginator will give you a list to deal with you paginator logic.

    [{'current': True, 'clickable': False, 'url_params': '/questions?a=1&page=1', 'text': 1}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=2', 'text': 2}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=3', 'text': 3}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=4', 'text': 4}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=5', 'text': 5}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=6', 'text': 6}, {'current': False, 'clickable': False, 'url_params': '', 'text': '...'}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=54', 'text': 54}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=2', 'text': u'Next'}]

Document
---

Paginator
---
Like django default Paginator, it rewrite page_range, and page.

init params:

    all Django Paginator params
    curr_page -- paginator current page num.
    display_pages -- if have 100 page, display_pages will only display the pages in page_range method.

rewrite method or property:

    page_range
        Default Django Paginator will return 1 to max page. [1..100]
        Here will use curr_page and display_pages to return the page_range.
        If max page is 100, display_pages is 5, curr_page is 10, the
        page_range will be [8, 9, 10, 11, 12].
        This is useful when handler front end paginator(or you can use a js lib).

    page
        In default Django Paginator page is a method.
        Here page is a property, it use curr_page to return Default Django page.

RequestPaginator
---

If you want to get page rang like, then Use RequestPaginator.

    Previous 1 ... 2 3 4 5 ... 3000 Next
    Previous 1 2 3 4 5 ... 3000 Next
    1 2 3 4 5 ... 3000 Next

Like Paginator, but in take some extra params to get the querystring page_params_range.

page_params_range: will return a list, each element is a dict, has those params:

    current: is current page or not
    clickable: can clickable
    url_params: /questions?a=1&page=1
    text: showing text



    [{'current': True, 'clickable': False, 'url_params': '/questions?a=1&page=1', 'text': 1}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=2', 'text': 2}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=3', 'text': 3}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=4', 'text': 4}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=5', 'text': 5}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=6', 'text': 6}, {'current': False, 'clickable': False, 'url_params': '', 'text': '...'}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=54', 'text': 54}, {'current': False, 'clickable': True, 'url_params': '/questions?a=1&page=2', 'text': u'Next'}]

Simple Usage
---

    from django.contrib.auth.models import User
    from paginator_plus.paginator import Paginator

    users = User.objects.all()
    print len(users)
    p = Paginator(users, per_page=2, curr_page=10)
    print p.page_range
    print

    p1 = Paginator(users, per_page=2, curr_page=20, display_pages=5)
    print p1.page_range
    print

    from django.http.request import HttpRequest, QueryDict

    r = HttpRequest()
    r.path_info = '/questions'
    r.GET = QueryDict('a=1')

    print
    print '========================='
    print

    from paginator_plus.paginator import RequestPaginator
    rp = RequestPaginator(users, per_page=2, curr_page=20, display_pages=5, request=r)
    print
    print 'rp = RequestPaginator(users, per_page=2, curr_page=20, display_pages=5, request=r)'
    print rp.page_range
    print rp.page_params_range,
    print

    rp1 = RequestPaginator(users, per_page=2, curr_page=20000, display_pages=5, request=r)
    print
    print 'rp1 = RequestPaginator(users, per_page=2, curr_page=20000, display_pages=5, request=r)'
    print rp1.page_range
    print rp.page_params_range,
    print

    rp3 = RequestPaginator(users, per_page=2, curr_page=1, display_pages=5, request=r)
    print
    print 'rp3 = RequestPaginator(users, per_page=2, curr_page=1, display_pages=5, request=r)'
    print rp3.page_range
    print rp3.page_params_range,
    print

    rp4 = RequestPaginator(users, per_page=2, curr_page=2, display_pages=5, request=r)
    print
    print 'rp4 = RequestPaginator(users, per_page=2, curr_page=2, display_pages=5, request=r)'
    print rp4.page_range
    print rp4.page_params_range,
    print

    rp5 = RequestPaginator(users, per_page=2, curr_page=2, display_pages=5, request=r, show_prev=False, show_next=False)
    print
    print 'rp5 = RequestPaginator(users, per_page=2, curr_page=2, display_pages=5, request=r, show_prev=False, show_next=False)'
    print rp5.page_range
    print rp5.page_params_range,
    print

    rp6 = RequestPaginator(users, per_page=2, curr_page=1, display_pages=6, request=r, auto_hide_prev=True)
    print
    print 'rp6 = RequestPaginator(users, per_page=2, curr_page=1, display_pages=6, request=r, auto_hide_prev=True)'
    print rp6.page_range
    print rp6.page_params_range,
    print

    rp7 = RequestPaginator(users, per_page=2, curr_page=2, display_pages=7, request=r, auto_hide_prev=True)
    print
    print 'rp7 = RequestPaginator(users, per_page=2, curr_page=2, display_pages=7, request=r, auto_hide_prev=True)'
    print rp7.page_range
    print rp7.page_params_range,
    print
