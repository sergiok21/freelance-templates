from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


def cache_home(view):
    return method_decorator(cache_page(60 * 30, key_prefix='home_page'), name='dispatch')(view)


def cache_portfolio(view):
    return method_decorator(cache_page(60 * 15, key_prefix='portfolio_page'), name='dispatch')(view)


def cache_condition(view):
    return method_decorator(cache_page(60 * 60, key_prefix='condition_page'), name='dispatch')(view)


def cache_category(view):
    return method_decorator(cache_page(60 * 20, key_prefix='category_page'), name='dispatch')(view)


def cache_contact(view):
    return method_decorator(cache_page(60 * 60, key_prefix='contact_page'), name='dispatch')(view)
