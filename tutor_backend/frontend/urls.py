from django.urls import path
from frontend.views import home_page, login_page, register_page, dashboard_page

urlpatterns = [
    path('', home_page, name='home-page'),
    path('login/', login_page, name='login-page'),
    path('register/', register_page, name='register-page'),
    path('dashboard/', dashboard_page, name='dashboard-page'),
]
