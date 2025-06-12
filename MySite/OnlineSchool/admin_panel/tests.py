from django.test import TestCase, Client
from django.urls import reverse
from main.models import Users, Students, Teachers, Courses
from django.contrib.auth.hashers import make_password

class AdminPanelTests(TestCase):
    def setUp(self):
        # Создаем тестового администратора
        self.admin = Users.objects.create(
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            password=make_password('Admin123!'),
            role='admin'
        )
        
        # Создаем тестового пользователя
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
        
        # Создаем тестовый клиент
        self.client = Client()
        
        # Авторизуем администратора
        self.client.session['user_id'] = self.admin.id_user

    def test_main_page_admin(self):
        """Тест главной страницы администратора"""
        response = self.client.get(reverse('admin_panel:main_page_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/main_page_admin.html')
        self.assertIn(self.user.first_name, response.content.decode())
        self.assertIn(self.user.last_name, response.content.decode())

    def test_add_user(self):
        """Тест добавления пользователя"""
        # Тест GET запроса
        response = self.client.get(reverse('admin_panel:add_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/add_user.html')
        
        # Тест POST запроса
        response = self.client.post(reverse('admin_panel:add_user'), {
            'role': 'student',
            'first_name': 'New',
            'last_name': 'Student',
            'email': 'new@example.com',
            'password': 'NewPass123!'
        })
        self.assertEqual(response.status_code, 302)  # Редирект после успешного добавления
        
        # Проверяем создание пользователя
        new_user = Users.objects.get(email='new@example.com')
        self.assertEqual(new_user.first_name, 'New')
        self.assertEqual(new_user.last_name, 'Student')
        self.assertEqual(new_user.role, 'student')

    def test_edit_user(self):
        """Тест редактирования пользователя"""
        # Тест GET запроса
        response = self.client.get(reverse('admin_panel:edit_user', args=[self.user.id_user]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_panel/edit_user.html')
        
        # Тест POST запроса
        response = self.client.post(reverse('admin_panel:edit_user', args=[self.user.id_user]), {
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

    def test_delete_user(self):
        """Тест удаления пользователя"""
        response = self.client.post(reverse('admin_panel:delete_user', args=[self.user.id_user]))
        self.assertEqual(response.status_code, 302)  # Редирект после успешного удаления
        
        # Проверяем удаление пользователя
        self.assertFalse(Users.objects.filter(id_user=self.user.id_user).exists())
        self.assertFalse(Students.objects.filter(is_user=self.user).exists())

    def test_export_teachers(self):
        """Тест экспорта данных преподавателей"""
        # Тест экспорта в Excel
        response = self.client.get(reverse('admin_panel:export_teachers_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
        # Тест экспорта в HTML
        response = self.client.get(reverse('admin_panel:export_teachers_html'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html')

    def test_unauthorized_access(self):
        """Тест доступа без авторизации администратора"""
        # Очищаем сессию
        self.client.session.flush()
        
        # Пробуем получить доступ к админ-панели
        response = self.client.get(reverse('authentication:login'))
        self.assertEqual(response.status_code, 200 )  # Редирект на страницу входа
