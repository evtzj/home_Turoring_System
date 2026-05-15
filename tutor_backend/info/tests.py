from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User,TeacherProfile
# Create your tests here.
class InfoApiTests(APITestCase):
    def setUp(self):
        self.teacher_list_url = reverse('teacher-list')
        self.teacher_user =User.objects.create_user(
            username='13800000024',
            phone='13800000024',
            password='abc12345',
            role='teacher',
        )
        TeacherProfile.objects.create(
            user=self.teacher_user,
            subject='数学',
            teaching_years=5,
            education='硕士',
        )

    def test_teacher_list_returns_teachers(self):
        response = self.client.get(self.teacher_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '查询成功')
        self.assertTrue(len(response.data['data']), 1)
        self.assertEqual(response.data['data'][0]['subject'],'数学')

    def test_teacher_detail_returns_teacher(self):
        teacher = TeacherProfile.objects.first()
        response = self.client.get(reverse('teacher-detail', args=[teacher.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '查询成功')
        self.assertEqual(response.data['data']['subject'], '数学')

    