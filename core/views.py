from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def recordings(request):
    return render(request, 'core/recordings.html')

def landings(request):
    return render(request, 'core/landings.html')

def customers(request):
    return render(request, 'core/customers.html')

def aircraft(request):
    return render(request, 'core/aircraft.html')

def invoices(request):
    return render(request, 'core/invoices.html')
