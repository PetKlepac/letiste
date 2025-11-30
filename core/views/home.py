from django.shortcuts import render, get_object_or_404, redirect
from ..models import Customer
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    return render(request, "core/home/home.html")