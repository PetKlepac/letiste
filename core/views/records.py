from django.shortcuts import render
from ..models import Record
from django.core.paginator import Paginator


def records(request):
    # Page number
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except:
        page = 1

    # Page size
    try:
        page_size = int(request.GET.get("size", 10))
    except:
        page_size = 10

    # Queryset
    records = Record.objects.order_by("-date_time")

    paginator = Paginator(records, page_size)
    records_page = paginator.get_page(page)

    return render(request, "core/records/records.html", {
        "records_list": records_page,
        "page_size": page_size,
        "page_sizes": [5, 10, 25, 50],
    })
