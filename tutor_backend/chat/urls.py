from django.urls import path
from chat.views import chat_of_match
urlpatterns=[
    path('matches/<int:match_id>/messages',chat_of_match,name='chat-if-match'),
]