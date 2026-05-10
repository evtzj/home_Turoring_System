from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from user.models import User


class UserApiFlowTests(APITestCase):
	def setUp(self):
		self.register_url = reverse('user-register')
		self.login_url = reverse('user-login')
		self.me_url = reverse('user-me')
		self.logout_url = reverse('user-logout')

	def test_register_success(self):
		payload = {
			'phone': '13800000021',
			'code': '123456',
			'password': 'abc12345',
			'role': 'student',
		}

		response = self.client.post(self.register_url, payload, format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data['message'], '注册成功')
		self.assertTrue(User.objects.filter(phone='13800000021').exists())

	def test_login_success_returns_token(self):
		User.objects.create_user(
			username='13800000022',
			phone='13800000022',
			password='abc12345',
			role='student',
		)

		payload = {
			'phone': '13800000022',
			'password': 'abc12345',
		}

		response = self.client.post(self.login_url, payload, format='json')

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], '登录成功')
		self.assertIn('token', response.data['data'])

	def test_me_requires_authentication(self):
		response = self.client.get(self.me_url)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_me_success_with_token(self):
		user = User.objects.create_user(
			username='13800000023',
			phone='13800000023',
			password='abc12345',
			role='student',
			first_name='Tom',
		)
		token = Token.objects.create(user=user)
		self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

		response = self.client.get(self.me_url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], '获取个人信息成功')
		self.assertEqual(response.data['data']['phone'], '13800000023')

	def test_logout_invalidates_token(self):
		user = User.objects.create_user(
			username='13800000024',
			phone='13800000024',
			password='abc12345',
			role='student',
		)
		token = Token.objects.create(user=user)
		self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

		logout_response = self.client.post(self.logout_url)
		me_response = self.client.get(self.me_url)

		self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
		self.assertEqual(logout_response.data['message'], '退出成功')
		self.assertEqual(me_response.status_code, status.HTTP_401_UNAUTHORIZED)
