from django.urls import path
from info.views import teacher_list, teacher_detail,favorite_teacher

urlpatterns = [
    path('teachers/', teacher_list, name='teacher-list'),
    path('teachers/<int:pk>/', teacher_detail, name='teacher-detail'),
    path('teachers/<int:pk>/favorite/', favorite_teacher, name='favorite-teacher'),
]
