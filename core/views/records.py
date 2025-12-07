from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import F
from ..models import Record


def records(request):

    # READ FILTERS (OR DEFAULT VALUES)
    filter_type = request.GET.get("filter", "probability")
    sort_order = request.GET.get("sort", "desc")
    date_query = request.GET.get("date", "").strip()
    page_size = int(request.GET.get("size", 25))
    page_number = request.GET.get("page")

    page_sizes = [25, 50, 100, 200]

    # BASE QUERY
    qs = Record.objects.all()

    # --- DATE FILTER ---
    if date_query:
        parts = date_query.split("-")
        try:
            if len(parts) == 1:
                qs = qs.filter(date_time__year=int(parts[0]))

            elif len(parts) == 2:
                qs = qs.filter(
                    date_time__year=int(parts[0]),
                    date_time__month=int(parts[1])
                )

            elif len(parts) == 3:
                qs = qs.filter(
                    date_time__year=int(parts[0]),
                    date_time__month=int(parts[1]),
                    date_time__day=int(parts[2])
                )
        except ValueError:
            pass  # invalid date, UI handles it

    # --- SORTING ---
    if filter_type == "probability":

        # Are there any non-null values?
        has_values = qs.exclude(detection_probability__isnull=True).exists()

        if has_values:
            if sort_order == "asc":
                qs = qs.order_by("detection_probability")
            else:
                qs = qs.order_by("-detection_probability")
        else:
            # All NULL → fallback ordering that doesn't reorder entries strangely
            qs = qs.order_by("id") if sort_order == "asc" else qs.order_by("-id")

    else:  # filter_type == "date"
        if sort_order == "asc":
            qs = qs.order_by("date_time")
        else:
            qs = qs.order_by("-date_time")

    # --- PAGINATION ---
    paginator = Paginator(qs, page_size)
    records_page = paginator.get_page(page_number)

    # ALWAYS RETURN RESPONSE
    return render(
        request,
        "core/records/records.html",
        {
            "records_list": records_page,
            "page_size": page_size,
            "page_sizes": page_sizes,
            "current_filter": filter_type,
            "current_sort": sort_order,
            "date_query": date_query,
        }
    )
