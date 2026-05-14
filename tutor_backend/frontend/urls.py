from django.urls import path
from frontend.views import login_page, register_page, dashboard_page

urlpatterns = [
    path('login/', login_page, name='login-page'),
    path('register/', register_page, name='register-page'),
    path('dashboard/', dashboard_page, name='dashboard-page'),
]
