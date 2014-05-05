
from django.core.paginator import (Paginator, 
                    EmptyPage, PageNotAnInteger)
from django.conf import settings
from rest_framework.pagination import PaginationSerializer

def paginate(request, list_result):
    paginator = Paginator(list_result, settings.PAGINATE_BY)
    page = request.QUERY_PARAMS.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    serializer = PaginationSerializer(instance=objects)
    return serializer.data
