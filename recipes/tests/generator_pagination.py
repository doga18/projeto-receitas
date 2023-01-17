import math
from django.core.paginator import Paginator


def make_pagination_range(
    page_range,
    qtd_paginas,
    current_page,
):
    middle_range = math.ceil(qtd_paginas / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qtd_paginas': qtd_paginas,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request, queryset, per_page, qtd_paginas=5):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginacao = Paginator(queryset, per_page)
    page_obj = paginacao.get_page(current_page)

    paginacao_range = make_pagination_range(
        paginacao.page_range,
        qtd_paginas,
        current_page
    )

    return page_obj, paginacao_range
