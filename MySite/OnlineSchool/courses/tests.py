from django.test import TestCase, Client
from django.urls import reverse
from main.models import Users, Students, Teachers, Courses, Lessons, RecordsStudents

class CoursesTests(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = Users.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='Test123!',
            role='student'
        )
        
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
            password='Test123!',
            role='teacher'
        )
        
        self.teacher = Teachers.objects.create(
            id_user=self.teacher_user,
            experience=5,
            rating=4.5
        )
        
        # Создаем тестовые курсы
        self.course1 = Courses.objects.create(
            course_name='Python Course',
            language_programming='Python',
            dfficulty_level=1,
            id_teacher=self.teacher,
            description='Python course description',
            duraction=3,
            price=1000
        )
        
        self.course2 = Courses.objects.create(
            course_name='Java Course',
            language_programming='Java',
            dfficulty_level=2,
            id_teacher=self.teacher,
            description='Java course description',
            duraction=4,
            price=2000
        )
        
        # Создаем тестовые уроки
        self.lesson1 = Lessons.objects.create(
            topic='Python Basics',
            video_url='https://example.com/video1.mp4',
            id_course=self.course1,
            lesson_number=1,
            status=True
        )
        
        self.lesson2 = Lessons.objects.create(
            topic='Python Advanced',
            video_url='https://example.com/video2.mp4',
            id_course=self.course1,
            lesson_number=2,
            status=False
        )
        
        # Создаем запись о прохождении курса
        self.record = RecordsStudents.objects.create(
            id_student=self.student,
            id_course=self.course1,
            status=True
        )
        
        # Создаем тестовый клиент
        self.client = Client()
        
        # Авторизуем пользователя
        self.client.session['user_id'] = self.user.id_user
        self.client.session['user_role'] = 'student'
        self.client.session['user_email'] = 'test@example.com'
        self.client.session['user_name'] = 'Test User'
        self.client.session.save()

    def test_courses_list(self):
        """Тест списка курсов"""
        # Тест базового отображения
        response = self.client.get(reverse('courses:courses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/courses.html')
        self.assertIn(self.course1.course_name, response.content.decode())
        self.assertIn(self.course2.course_name, response.content.decode())
        
        # Тест фильтрации по языку
        response = self.client.get(reverse('courses:courses') + '?language=Python')
        self.assertIn(self.course1.course_name, response.content.decode())
        self.assertNotIn(self.course2.course_name, response.content.decode())
        
        # Тест фильтрации по сложности
        response = self.client.get(reverse('courses:courses') + '?difficulty=1')
        self.assertIn(self.course1.course_name, response.content.decode())
        self.assertNotIn(self.course2.course_name, response.content.decode())
        
        # Тест поиска
        response = self.client.get(reverse('courses:courses') + '?search=Python')
        self.assertIn(self.course1.course_name, response.content.decode())
        self.assertNotIn(self.course2.course_name, response.content.decode())
        
 
        # Тест сортировки по цене (по возрастанию)
        response = self.client.get(reverse('courses:courses') + '?sort=price-asc')
        content = response.content.decode()
        self.assertTrue(content.find(self.course1.course_name) < content.find(self.course2.course_name))

    def test_about_course(self):
        """Тест страницы информации о курсе"""
        response = self.client.get(reverse('courses:about_course', args=[self.course1.id_course]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/about_course.html')
        
        content = response.content.decode()
        self.assertIn(self.course1.course_name, content)
        self.assertIn(self.course1.description, content)
        self.assertIn(str(self.course1.price), content)
        self.assertIn(self.teacher_user.first_name, content)
        self.assertIn(self.teacher_user.last_name, content)
        
        # Проверяем отображение уроков
        self.assertIn(self.lesson1.topic, content)
        self.assertIn(self.lesson2.topic, content)

    def test_current_course(self):
        """Тест страницы текущего курса"""
        response = self.client.get(reverse('courses:current_course', args=[self.course1.id_course]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/current_course.html')
        
        content = response.content.decode()
        self.assertIn(self.course1.course_name, content)
        self.assertIn(self.course1.description, content)
        self.assertIn(str(self.course1.duraction), content)
        
        # Проверяем отображение уроков
        self.assertIn(self.lesson1.topic, content)
        self.assertIn(self.lesson2.topic, content)
        
        # Проверяем статус уроков
        self.assertIn('block', content)

    def test_lesson(self):
        """Тест страницы урока"""
        response = self.client.get(reverse('courses:lesson', args=[self.lesson1.id_lesson]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/lesson.html')
        
        content = response.content.decode()
        self.assertIn(self.lesson1.topic, content)
        self.assertIn(self.lesson1.video_url, content)
        

    def test_unauthorized_access(self):
        """Тест доступа без авторизации"""
        # Очищаем сессию
        self.client.session.flush()
        
        # Пробуем получить доступ к страницам
        response = self.client.get(reverse('courses:courses'))
        self.assertEqual(response.status_code, 200)  # Список курсов доступен всем
        
        response = self.client.get(reverse('courses:about_course', args=[self.course1.id_course]))
        self.assertEqual(response.status_code, 200)  # Информация о курсе доступна всем 
        
        response = self.client.get(reverse('courses:lesson', args=[self.lesson1.id_lesson]))
        self.assertEqual(response.status_code, 200)  # Урок доступен всем