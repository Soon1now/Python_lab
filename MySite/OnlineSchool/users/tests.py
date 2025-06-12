from django.test import TestCase, Client
from django.urls import reverse
from main.models import Users, Students, Courses, RecordsStudents
from django.contrib.auth.hashers import make_password

class UsersAppTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя с хешированным паролем
        self.user = Users.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password=make_password('Test123!'),
            role='student'
        )
        
        # Создаем тестового студента
        self.student = Students.objects.create(
            is_user=self.user,
            count_course=0
        )
        
        # Создаем тестовый курс
        self.course = Courses.objects.create(
            course_name='Test Course',
            language_programming='Python',
            dfficulty_level=1,
            description='Test course description',
            duraction=3,
            price=1000
        )
        
        # Создаем запись о курсе студента
        self.record = RecordsStudents.objects.create(
            id_student=self.student,
            id_course=self.course,
            status=True
        )
        
        # Создаем тестовый клиент
        self.client = Client()
        
        # Авторизуем пользователя
        session = self.client.session
        session['user_id'] = self.user.id_user
        session['user_role'] = self.user.role
        session['user_email'] = self.user.email
        session['user_name'] = f"{self.user.first_name} {self.user.last_name}"
        session.save()

    def test_account_page(self):
        """Тест страницы личного кабинета"""
        response = self.client.get(reverse('users:account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/account.html')
    
        # Проверяем, что имя пользователя отображается
        # Имя и фамилия отображаются отдельно
        self.assertIn(self.user.first_name, response.content.decode())
        self.assertIn(self.user.last_name, response.content.decode())
    
        # Проверяем название курса
        self.assertIn(self.course.course_name, response.content.decode())
    
    def test_edit_profile(self):
        """Тест редактирования профиля"""
        # Тест GET запроса
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')
        
        # Тест POST запроса
        response = self.client.post(reverse('users:edit_profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'password': 'NewPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после успешного обновления
        
        # Проверяем обновленные данные
        updated_user = Users.objects.get(id_user=self.user.id_user)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'Name')
        self.assertEqual(updated_user.email, 'updated@example.com')

    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        # Очищаем сессию
        self.client.session.flush()
        
        # Пробуем получить доступ к личному кабинету
        response = self.client.get(reverse('users:account'))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа
        
        # Пробуем получить доступ к редактированию профиля
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа
