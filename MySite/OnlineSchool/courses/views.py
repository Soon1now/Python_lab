from django.shortcuts import render, get_object_or_404
from main.models import Courses, Lessons, Teachers, Users, RecordsStudents, Students


def courses(request):
    language = request.GET.get('language', '')
    difficulty = request.GET.get('difficulty', '')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')

    courses_list = Courses.objects.all()

    if language:
        courses_list = courses_list.filter(language_programming=language)
    if difficulty:
        courses_list = courses_list.filter(dfficulty_level=difficulty)
    if search:
        courses_list = courses_list.filter(course_name__icontains=search)

    # Сортировка
    if sort == 'a-z':
        courses_list = courses_list.order_by('course_name')
    elif sort == 'z-a':
        courses_list = courses_list.order_by('-course_name')
    elif sort == 'price-asc':
        courses_list = courses_list.order_by('price')
    elif sort == 'price-desc':
        courses_list = courses_list.order_by('-price')

    languages = Courses.objects.values_list('language_programming', flat=True).distinct()
    difficulties = Courses.objects.values_list('dfficulty_level', flat=True).distinct()
    prices = Courses.objects.values_list('price', flat=True).distinct()
    
    context = {
        'courses': courses_list,
        'selected_language': language,
        'selected_difficulty': difficulty,
        'languages': languages,
        'difficulties': difficulties,
        'prices': prices,
    }
    return render(request, 'courses/courses.html', context)

def lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id_lesson=lesson_id)
    course = lesson.id_course if hasattr(lesson, 'id_course') else None
    teacher_info = None
    
    if course and hasattr(course, 'id_teacher') and course.id_teacher:
        try:
            teacher_id = course.id_teacher.id_teacher if hasattr(course.id_teacher, 'id_teacher') else course.id_teacher
            teacher = Teachers.objects.get(id_teacher=teacher_id)
            teacher_user_id = teacher.id_user.id_user if hasattr(teacher.id_user, 'id_user') else teacher.id_user
            teacher_user = Users.objects.get(id_user=teacher_user_id)
            teacher_info = {
                'full_name': f"{teacher_user.first_name} {teacher_user.last_name}",
                'experience': teacher.experience,
                'rating': teacher.rating
            }
        except (Teachers.DoesNotExist, Users.DoesNotExist, AttributeError):
            teacher_info = None
    
    context = {
        'lesson': lesson,
        'course': course,
        'teacher': teacher_info
    }
    return render(request, 'courses/lesson.html', context)

def current(request, course_id):
    try:
        course = get_object_or_404(Courses, id_course=course_id)
        lessons = Lessons.objects.filter(id_course=course_id).order_by('lesson_number')
        active_lessons = [lesson for lesson in lessons if getattr(lesson, 'status', False)]
        
        if active_lessons:
            last_active_lesson = max(active_lessons, key=lambda l: l.lesson_number)

        teacher_info = None
        if course.id_teacher:
            try:
                teacher_id = course.id_teacher.id_teacher if hasattr(course.id_teacher, 'id_teacher') else course.id_teacher
                teacher = Teachers.objects.get(id_teacher=teacher_id)
                teacher_user_id = teacher.id_user.id_user if hasattr(teacher.id_user, 'id_user') else teacher.id_user
                teacher_user = Users.objects.get(id_user=teacher_user_id)
                teacher_info = {
                    'full_name': f"{teacher_user.first_name} {teacher_user.last_name}",
                    'experience': teacher.experience,
                    'rating': teacher.rating
                }
            except (Teachers.DoesNotExist, Users.DoesNotExist, AttributeError) as e:
                print(f"Ошибка при получении данных преподавателя: {str(e)}")
                teacher_info = None
        
        student_progress = None
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = Users.objects.get(id_user=user_id)
                if user.role == 'student':
                    student = Students.objects.get(is_user=user)
                    record = RecordsStudents.objects.filter(id_student=student, id_course=course).first()
                    if record:
                        student_progress = {
                            'status': 'active' if record.status else 'completed',
                        }
            except (Users.DoesNotExist, Students.DoesNotExist, RecordsStudents.DoesNotExist):
                pass
        
        context = {
            'course': {
                'id': course.id_course,
                'name': course.course_name,
                'description': course.description,
                'language': course.language_programming,
                'difficulty': course.dfficulty_level,
                'duration': course.duraction,
                'price': course.price,
            },
            'lessons': [{
                'id': lesson.id_lesson,
                'number': lesson.lesson_number,
                'title': lesson.topic,
                'video': lesson.video_url if lesson.video_url else None,
                'description': lesson.description if hasattr(lesson, 'description') else None,
                'status': lesson.status if hasattr(lesson, 'status') else None
            } for lesson in lessons],
            'teacher': teacher_info,
            'student_progress': student_progress
        }
        
        return render(request, 'courses/current_course.html', context)
    except Exception as e:
        print(f"Ошибка при получении данных о курсе: {str(e)}")
        return render(request, 'courses/error.html', {
            'error_message': 'Курс не найден или произошла ошибка',
            'error_details': str(e)
        })

def about_course(request, course_id):
    try:
        # Получаем курс или возвращаем 404 если не найден
        course = get_object_or_404(Courses, id_course=course_id)
        
        # Получаем все уроки этого курса
        lessons = Lessons.objects.filter(id_course=course_id)
        
        # Получаем информацию о преподавателе
        teacher_info = None
        if course.id_teacher:
            try:
                # Преобразуем id_teacher в число, если это объект
                teacher_id = course.id_teacher.id_teacher if hasattr(course.id_teacher, 'id_teacher') else course.id_teacher
                teacher = Teachers.objects.get(id_teacher=teacher_id)
                # Получаем id пользователя как число
                teacher_user_id = teacher.id_user.id_user if hasattr(teacher.id_user, 'id_user') else teacher.id_user
                teacher_user = Users.objects.get(id_user=teacher_user_id)
                teacher_info = {
                    'full_name': f"{teacher_user.first_name} {teacher_user.last_name}",
                    'experience': teacher.experience,
                    'rating': teacher.rating
                }
            except (Teachers.DoesNotExist, Users.DoesNotExist, AttributeError) as e:
                print(f"Ошибка при получении данных преподавателя: {str(e)}")
                teacher_info = None
        
        context = {
            'course': {
                'id': course.id_course,
                'name': course.course_name,
                'description': course.description,
                'language': course.language_programming,
                'difficulty': course.dfficulty_level,
                'duraction': course.duraction,
                'price': course.price,
            },
            'lessons': [{
                'id': lesson.id_lesson,
                'number': lesson.lesson_number,
                'title': lesson.topic,
                'video': lesson.video_url if lesson.video_url else None,
                
            } for lesson in lessons],
            'teacher': teacher_info
        }
        
        return render(request, 'courses/about_course.html', context)
        
    except Exception as e:
        print(f"Ошибка при получении данных о курсе: {str(e)}")
        return render(request, 'courses/error.html', {
            'error_message': 'Курс не найден или произошла ошибка',
            'error_details': str(e)
        })