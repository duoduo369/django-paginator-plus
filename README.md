django-paginator-plus
===

Save extra data to django paginator.
Useful when url has params.

What to save the url params and get a format page_range?

http://myhost/something?page=10&a=1 --> [?page=8&a=1, ?page=9&a=1, ?page=10&a=1, ?page=11&a=1, ?page=12&a=1]

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
Like Paginator, but in take some extra params to get the querystring page_range.

page_range is like Paginator.page_range, but it not only return a number list.
It will has querystring too, like [?page=8&a=1, ?page=9&a=1, ?page=10&a=1, ?page=11&a=1, ?page=12&a=1].
This is useful when handler front end paginator(or you can use a js lib).

Simple Usage
---

    from django.contrib.auth.models import User
    from paginator_plus.paginator import Paginator

    users = User.objects.all()
    print len(users)
    p = Paginator(users, per_page=2, curr_page=10)
    print p.page_range

    p1 = Paginator(users, per_page=2, curr_page=20, display_pages=5)
    print p1.page_range

    from django.http.request import HttpRequest, QueryDict

    r = HttpRequest()
    r.path_info = '/questions'
    r.GET = QueryDict('a=1')

    from paginator_plus.paginator import RequestPaginator
    rp = RequestPaginator(users, per_page=2, curr_page=20, display_pages=5, request=r)
    print rp.page_range

    rp1 = RequestPaginator(users, per_page=2, curr_page=20000, display_pages=5, request=r)
    print rp1.page_range
