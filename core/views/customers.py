from django.shortcuts import render, get_object_or_404, redirect
from ..models import Customer, Aircraft
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator


def customers(request):
    # URL parameters
    search_query = request.GET.get("search", "")
    filter_field = request.GET.get("filter", "name")
    sort_dir = request.GET.get("sort", "asc")
    # Safe page handling
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            page = 1
    except:
        page = 1
    page_size = int(request.GET.get("size", 25))

    # Base queryset
    customers = Customer.objects.select_related("user")

    # Filtering
    if search_query:
        if filter_field == "id":
            customers = customers.filter(id__icontains=search_query)
        elif filter_field == "name":
            customers = customers.filter(user__username__icontains=search_query)
        elif filter_field == "email":
            customers = customers.filter(user__email__icontains=search_query)
        elif filter_field == "company":
            customers = customers.filter(company_name__icontains=search_query)

    # Sorting
    order_map = {
        "id": "id",
        "name": "user__username",
        "email": "user__email",
        "company": "company_name",
    }

    order_field = order_map.get(filter_field, "id")
    if sort_dir == "desc":
        order_field = "-" + order_field

    customers = customers.order_by(order_field)

    # Pagination
    paginator = Paginator(customers, page_size)
    customers_page = paginator.get_page(page)

    # Render
    return render(request, "core/customers/customers.html", {
        "customers_list": customers_page,
        "page_size": page_size,
        "page_sizes": [10, 25, 50, 100],
        "search_query": search_query,
        "current_filter": filter_field,
        "current_sort": sort_dir,
    })


User = get_user_model()  # ← správne pre custom user model


# TODO what if username already exists
def add_customer(request):
    if request.method == "POST":
        # USER FIELDS
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        street = request.POST.get("street")
        city = request.POST.get("city")
        postal_code = request.POST.get("postal_code")
        country = request.POST.get("country")

        # CUSTOMER FIELDS
        company = request.POST.get("company_name")
        vat = request.POST.get("vat_id")
        note = request.POST.get("note")

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # Save personal data
        user.phone_number = phone
        user.street = street
        user.city = city
        user.postal_code = postal_code
        user.country = country
        user.save()

        # Create Customer
        Customer.objects.create(
            user=user,
            company_name=company,
            vat_id=vat,
            note=note
        )

        return redirect("customers")

    return redirect("customers")


def edit_customer(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.phone_number = request.POST.get("phone")
        user.street = request.POST.get("street")
        user.city = request.POST.get("city")
        user.postal_code = request.POST.get("postal_code")
        user.country = request.POST.get("country")
        user.save()

        return redirect("customers")

    return redirect("customers")


def update_customer(request):
    if request.method == "POST":

        customer_id = request.POST.get("customer_id")
        customer = get_object_or_404(Customer, id=customer_id)
        user = customer.user

        # User fields
        user.username = request.POST.get("username") or ""
        user.email = request.POST.get("email") or ""
        user.phone_number = request.POST.get("phone") or ""
        user.street = request.POST.get("street") or ""
        user.city = request.POST.get("city") or ""
        user.postal_code = request.POST.get("postal_code") or ""
        user.country = request.POST.get("country") or ""
        user.save()

        # Customer fields
        customer.company_name = request.POST.get("company_name") or ""
        customer.vat_id = request.POST.get("vat_id") or ""
        customer.note = request.POST.get("note") or ""
        customer.save()

        messages.success(request, "Zákazník byl úspěšně aktualizován.")

        # Pokud jsme přišli z detailu → vrať se tam
        if request.POST.get("return_to_detail") == "1":
            return redirect("customer_detail", customer.id)

        # Jinak klasicky zpět na seznam
        return redirect("customers")


def delete_customer(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        customer = get_object_or_404(Customer, id=customer_id)

        # Zmažeme usera → tým sa automaticky zmaže Customer (OneToOne + CASCADE)
        user = customer.user
        user.delete()

        messages.success(request, "Zákazník bol úspešne odstránený.")
        return redirect("customers")


def customer_detail(request, pk):
    customer = get_object_or_404(Customer.objects.select_related("user"), id=pk)
    return render(request, "core/customers/customer_detail.html", {
        "customer": customer
    })


def add_aircraft(request, customer_id):
    if request.method == "POST":
        customer = get_object_or_404(Customer, id=customer_id)

        registration = request.POST.get("registration")
        name = request.POST.get("name")

        Aircraft.objects.create(
            registration=registration,
            name=name,
            owner=customer
        )

        messages.success(request, "Letadlo bylo úspěšně přidáno.")

        return redirect("customer_detail", pk=customer_id)


def edit_aircraft(request):
    if request.method == "POST":
        aircraft_id = request.POST.get("aircraft_id")
        aircraft = get_object_or_404(Aircraft, id=aircraft_id)

        aircraft.registration = request.POST.get("registration")
        aircraft.name = request.POST.get("name")
        aircraft.save()

        messages.success(request, "Letadlo bylo aktualizováno.")

        return redirect("customer_detail", pk=aircraft.owner.id)


def delete_aircraft(request):
    if request.method == "POST":
        aircraft_id = request.POST.get("aircraft_id")
        aircraft = get_object_or_404(Aircraft, id=aircraft_id)

        customer_id = aircraft.owner.id if aircraft.owner else None
        aircraft.delete()

        messages.success(request, "Letadlo bylo odstraněno.")

        return redirect("customer_detail", pk=customer_id)



