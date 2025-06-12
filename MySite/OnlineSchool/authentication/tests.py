from django.test import TestCase, Client
from django.urls import reverse
from main.models import Users
from django.core import mail

class AuthenticationTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = Users.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='Test123!',  # Пароль не хешируется
            role='student'
        )
        
        # Создаем тестовый клиент
        self.client = Client()

    def test_password_reset(self):
        """Тест сброса пароля"""
        # Тест запроса сброса пароля
        response = self.client.post(reverse('authentication:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после отправки
        
        # Проверяем отправку email
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['test@example.com'])
        
        # Получаем токен из базы данных
        user = Users.objects.get(email='test@example.com')
        
        # Тестируем установку нового пароля
        response = self.client.post(reverse('authentication:password_reset_confirm', args=[user.reset_token]), {
            'new_password': 'NewPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после успешной смены пароля
        
        # Обновляем данные пользователя из базы
        user.refresh_from_db()
        self.assertTrue(user.check_password('NewPass123!'))

   