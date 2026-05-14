from django.urls import path
from match.views import list_or_create_match,match_confirm,match_detail
urlpatterns=[
    path('matches/',list_or_create_match,name='match-list-create'),
    path('matches/<int:pk>/',match_detail,name='match-detail'),
    path('matches/<int:pk>/confirm/',match_confirm,name='match-confirm'),
]