from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_list(entity_list, page, page_size):
    paginator = Paginator(entity_list, page_size)
    try:
        entities = paginator.page(page)
    except PageNotAnInteger:
        entities = paginator.page(1)
    except EmptyPage:
        entities = paginator.page(paginator.num_pages)

    return entities


