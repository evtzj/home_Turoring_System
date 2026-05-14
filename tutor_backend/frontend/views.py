from django.shortcuts import render


def login_page(request):
    return render(request, 'frontend/login.html')


def register_page(request):
    return render(request, 'frontend/register.html')


def dashboard_page(request):
    return render(request, 'frontend/dashboard.html')
