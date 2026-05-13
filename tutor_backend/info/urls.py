from django.urls import path
from info.views import teacher_list, teacher_detail

urlpatterns = [
    path('teachers/', teacher_list, name='teacher-list'),
    path('teachers/<int:pk>/', teacher_detail, name='teacher-detail'),
]
