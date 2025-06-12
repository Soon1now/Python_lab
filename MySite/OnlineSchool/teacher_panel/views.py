from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Courses, Lessons, Tasks, TaskExecution, Users, Teachers
from django.core.exceptions import PermissionDenied


def teacher_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Пожалуйста, войдите в систему')
        return redirect('authentication:login')
    
    try:
        user = Users.objects.get(id_user=user_id)
        teacher = Teachers.objects.filter(id_user=user.id_user).first()
        if not teacher:
            raise Teachers.DoesNotExist
        
        # Получаем все курсы преподавателя с количеством уроков
        courses = Courses.objects.filter(id_teacher=teacher.id_teacher)
        for course in courses:
            course.lesson_count = Lessons.objects.filter(id_course=course.id_course).count()
        
        context = {
            'user': user,
            'teacher': teacher,
            'courses': courses,
        }
    except Users.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
        return redirect('authentication:login')
    except Exception as e:
        print(f"Error: {str(e)}")
        messages.error(request, 'Произошла ошибка при загрузке данных')
        return redirect('authentication:login')
    
    return render(request, 'teacher_panel/dashboard.html', context)

def task(request):
    user_id = request.session.get('user_id')
    print(f"User ID: {user_id}")  # Лог для отладки
    
    try:
        user = Users.objects.get(id_user=user_id)
        print(f"User found: {user.first_name} {user.last_name}")  # Лог для отладки
        
        teacher = Teachers.objects.filter(id_user=user.id_user).first()
        print(f"Teacher ID: {teacher.id_teacher if teacher else 'None'}")  # Лог для отладки
        
        if not teacher:
            raise Teachers.DoesNotExist
        
        courses = Courses.objects.filter(id_teacher=teacher.id_teacher)
        print(f"Found {courses.count()} courses")  # Лог для отладки
        
        lessons = Lessons.objects.filter(id_course__in=courses)
        print(f"Found {lessons.count()} lessons")  # Лог для отладки
        
        tasks = Tasks.objects.filter(
            id_lesson__in=lessons.values('id_lesson')
        )
        print(f"Found {tasks.count()} tasks")  # Лог для отладки
        
        context = {
            'user': user,
            'teacher': teacher,
            'tasks': tasks,
            'courses': courses,
            'name': user.first_name,
        }
        return render(request, 'teacher_panel/task.html', context)
    except Exception as e:
        print(f"Error: {str(e)}")  # Лог для отладки
        messages.error(request, f'Ошибка: {str(e)}')
        return redirect('teacher_panel:dashboard')  # Исправляем редирект

'''@login_required
def teacher_courses(request):
    user = request.user
    if not hasattr(user, 'teacher'):
        raise PermissionDenied("Access denied")
    
    courses = Courses.objects.filter(id_teacher=user.teacher)
    context = {
        'courses': courses,
        'user': user
    }
    return render(request, 'teacher_panel/courses.html', context)

@login_required
def course_detail(request, course_id):
    user = request.user
    if not hasattr(user, 'teacher'):
        raise PermissionDenied("Access denied")
    
    course = get_object_or_404(Courses, id_course=course_id, id_teacher=user.teacher)
    lessons = Lessons.objects.filter(id_course=course)
    
    if request.method == 'POST':
        # Handle lesson material upload
        lesson_id = request.POST.get('lesson_id')
        lesson = get_object_or_404(Lessons, id_lesson=lesson_id)
        
        if 'video_url' in request.POST:
            lesson.video_url = request.POST['video_url']
        if 'material' in request.FILES:
            lesson.material = request.FILES['material']
        
        lesson.save()
        messages.success(request, 'Материалы успешно обновлены')
        return redirect('teacher_panel:course_detail', course_id=course_id)
    
    context = {
        'course': course,
        'lessons': lessons,
        'user': user
    }
    return render(request, 'teacher_panel/course_detail.html', context)

@login_required
def assignments(request):
    user = request.user
    if not hasattr(user, 'teacher'):
        raise PermissionDenied("Access denied")
    
    teacher_courses = Courses.objects.filter(id_teacher=user.teacher)
    assignments = Assignments.objects.filter(id_lesson__id_course__in=teacher_courses)
    
    context = {
        'assignments': assignments,
        'user': user
    }
    return render(request, 'teacher_panel/assignments.html', context)

@login_required
def check_assignment(request, assignment_id):
    user = request.user
    if not hasattr(user, 'teacher'):
        raise PermissionDenied("Access denied")
    
    assignment = get_object_or_404(Assignments, id_assignment=assignment_id)
    if assignment.id_lesson.id_course.id_teacher != user.teacher:
        raise PermissionDenied("Access denied")
    
    if request.method == 'POST':
        grade = request.POST.get('grade')
        comment = request.POST.get('comment')
        
        assignment.grade = grade
        assignment.teacher_comment = comment
        assignment.is_checked = True
        assignment.save()
        
        messages.success(request, 'Оценка успешно поставлена')
        return redirect('teacher_panel:assignments')
    
    context = {
        'assignment': assignment,
        'user': user
    }
    return render(request, 'teacher_panel/check_assignment.html', context)'''