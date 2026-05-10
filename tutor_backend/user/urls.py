from django.urls import path
from user.views import register_view,login_view,me_view,logout_view
urlpatterns=[
    path('register/',register_view,name='user-register'),
    path('login/', login_view, name='user-login'),
    path("me/",me_view,name="user-me"),
    path("logout/",logout_view,name="user-logout"),
]