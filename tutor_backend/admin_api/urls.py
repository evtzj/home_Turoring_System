from django.urls import path
from admin_api.views import list_users,user_detail,check_teacher,count_stats
urlpatterns=[
    path('users/', list_users, name='list-users'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('teachers/<int:pk>/check/', check_teacher, name='check-teacher'),
    path('stats/', count_stats, name='count-stats'),
]