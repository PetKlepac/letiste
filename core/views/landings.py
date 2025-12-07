from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from ..models import Landing

def landings(request):

    sort_order = request.GET.get("sort", "desc")
    date_query = request.GET.get("date", "").strip()
    page_size = int(request.GET.get("size", 25))
    page_number = request.GET.get("page")

    page_sizes = [10, 25, 50, 100]

    qs = Landing.objects.all()

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
            pass

    # --- SORTING ---
    if sort_order == "asc":
        qs = qs.order_by("date_time")
    else:
        qs = qs.order_by("-date_time")

    # --- PAGINATION ---
    paginator = Paginator(qs, page_size)
    landings_page = paginator.get_page(page_number)

    return render(
        request,
        "core/landings/landings.html",
        {
            "landings_list": landings_page,
            "page_size": page_size,
            "page_sizes": page_sizes,
            "current_sort": sort_order,
            "date_query": date_query,
        }
    )

def add_landing(request):
    # Dočasný placeholder, aby šablóna fungovala
    return HttpResponse("Formulář pro přidání přistání bude zde.")


def landing_detail(request, pk):
    # Dočasný placeholder
    return HttpResponse(f"Detail přistání #{pk} bude zde.")
