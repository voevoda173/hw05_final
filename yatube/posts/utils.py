from django.core.paginator import Paginator

from .constants import POSTS_AMOUNT


def pagin(request, posts):
    """ Функция-утилита для деления постов по страницам."""
    paginator = Paginator(posts, POSTS_AMOUNT)
    page_number = request.GET.get('page')
    paginator.get_page(page_number)

    return paginator.get_page(page_number)
