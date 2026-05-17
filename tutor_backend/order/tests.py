from rest_framework.test import APITestCase
from django.urls import reverse
from user.models import User
from user.models import TeacherProfile
# Create your tests here.
class OrderApiFlowTests (APITestCase):
    def setUp(self):
        self.order_list_url = reverse('create-order')
        self.student_user = User.objects.create_user(
            username='13800000025',
            phone='13800000025',
            password='abc12345',
            role='student',
        )
        self.teacher_user = User.objects.create_user(
            username='13800000026',
            phone='13800000026',
            password='abc12345',
            role='teacher',
        )
        TeacherProfile.objects.create(
            user=self.teacher_user,
            subject='数学',
            teaching_years=5,
            education='硕士',
        )
    def test_create_order(self):
        self.client.force_authenticate(user = self.student_user)
        payload = {
            'teacher_id': self.teacher_user.teacherprofile.id,
            'subject': '数学',
            'student':'学生一',
            'scheduled_time':'2024-07-01T10:00:00Z',
            'duration': 60,
            'price': 200.00,
            'address': '北京市海淀区',
            'remarks': '请提前准备教材',

        }
        response = self.client.post(self.order_list_url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], '订单创建成功')
        
    def test_list_orders(self):
        self.client.force_authenticate(user = self.student_user)
        response = self.client.get(self.order_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], '订单列表获取成功')

    def test_order_detail(self):
        self.client.force_authenticate(user = self.student_user)
        # 创建订单
        payload = {
            'teacher_id': self.teacher_user.teacherprofile.id,
            'subject': '数学',
            'student':'学生一',
            'scheduled_time':'2024-07-01T10:00:00Z',
            'duration': 60,
            'price': 200.00,
            'address': '北京市海淀区',
            'remarks': '请提前准备教材',

        }
        create_response = self.client.post(self.order_list_url, payload, format='json')
        order_id = create_response.data['data']['id']
        # 获取订单详情
        order_detail_url = reverse('order-detail', args=[order_id])
        detail_response = self.client.get(order_detail_url)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(detail_response.data['message'], '订单详情获取成功')