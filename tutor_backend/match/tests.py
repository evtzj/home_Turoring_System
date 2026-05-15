from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User,TeacherProfile
from match.models import Match
# Create your tests here.
class MatchApiTests(APITestCase):
    def setUp(self):
        self.match_list_url = reverse('match-list')
        self.student_user =User.objects.create_user(
            username='13800000025',
            phone='13800000025',
            password='abc12345',
            role='student',
        )
        self.teacher_user =User.objects.create_user(
            username='13800000026',
            phone='13800000026',
            password='abc12345',
            role='teacher',
        )
        TeacherProfile.objects.create(
            user=self.teacher_user,
            subject='英语',
            teaching_years=3,
            education='本科',
        )

    def test_match_list_returns_matches(self):
        response = self.client.get(self.match_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_match_detail(self):
        match = Match.objects.create(
            student = self.student_user,
            teacher = TeacherProfile.objects.first(),
            subject = '英语',
            grade = '高中',
            city = '上海',
            status = 'pending',
        )
        response = self.client.get(reverse('match-detail', args=[match.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '查询成功')
        self.assertEqual(response.data['data']['subject'], '英语')
        self.assertEqual(response.data['data']['grade'], '高中')
        self.assertEqual(response.data['data']['city'], '上海')
        self.assertEqual(response.data['data']['status'], 'pending')

    def test_match_confirm(self):
        match = Match.objects.create(
            student = self.student_user,
            teacher = TeacherProfile.objects.first(),
            subject = '英语',
            grade = '高中',
            city = '上海',
            status = 'pending',
        )
        response = self.client.post(reverse('match-confirm', args=[match.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '匹配已确认')
        match.refresh_from_db()
        self.assertEqual(match.status, 'confirmed')

    def test_match_create(self):
        payload = {
            'teacher_id': TeacherProfile.objects.first().id,
            'subject': '英语',
            'grade': '高中',
            'city': '上海',
        }
        response = self.client.post(self.match_list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], '匹配创建成功')
        self.assertTrue(Match.objects.filter(student=self.student_user).exists())