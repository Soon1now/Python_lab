# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Users, Students, Courses, Teachers
from django.contrib.auth.hashers import make_password

class MainAppTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.password = 'Test123!'
        self.user = Users.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password=self.password,
            role='student'
        )
        self.user.set_password(self.password)
        # Создаем тестового студента
        self.student = Students.objects.create(
            is_user=self.user,
            count_course=0
        )
        
        # Создаем тестового преподавателя
        self.teacher_user = Users.objects.create(
            first_name='Teacher',
            last_name='Test',
            email='teacher@example.com',
            password=self.password,
            role='teacher'
        )
        
        # Создаем клиент для тестирования
        self.client = Client()

    def test_index_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')  # Прямой путь вместо reverse
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/main_page.html')

    def test_user_creation(self):
        """Тест создания пользователя"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'student')
        # Проверяем пароль с сохраненным значением
        self.assertTrue(self.user.check_password(self.password))
