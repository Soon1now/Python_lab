from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import Users, Students, RecordsStudents, Courses
from django.contrib.auth.hashers import make_password

# Create your views here.

def account(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'Пожалуйста, войдите в систему')
        return redirect('authentication:login')
    
    try:
        user = Users.objects.get(id_user=user_id)
        
        student_data = None
        active_courses = []
        completed_courses = []
        
        if user.role == 'student':
            student_data = Students.objects.get(is_user=user)
            records = RecordsStudents.objects.filter(id_student=student_data)
            
            for record in records:
                course = record.id_course
                course_data = {
                    'id': course.id_course,
                    'course_name': course.course_name,
                    'language_programming': course.language_programming,
                    'duraction': course.duraction,
                    'progress': getattr(record, 'progress', 0),
                    'status': 'active' if record.status else 'completed',
                }
                
                if record.status:
                    active_courses.append(course_data)
                else:
                    completed_courses.append(course_data)
        
        context = {
            'user': user,
            'student_data': student_data,
            'active_courses': active_courses,
            'completed_courses': completed_courses
        }
        
        return render(request, 'users/account.html', context)
        
    except (Users.DoesNotExist, Students.DoesNotExist) as e:
        messages.error(request, f'Ошибка при получении данных пользователя: {str(e)}')
        return redirect('authentication:login')

def edit_profile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, 'Пожалуйста, войдите в систему')
        return redirect('authentication:login')
    
    try:
        user = Users.objects.get(id_user=user_id)
        
        if request.method == 'POST':
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.patronymic = request.POST.get('patronymic')
            user.number_phone = request.POST.get('number_phone')

            password = request.POST.get('password')
            if password:
                user.password = password
            
            try:
                user.save()
                messages.success(request, 'Профиль успешно обновлен')
                return redirect('users:account')
            except Exception as e:
                messages.error(request, f'Ошибка при обновлении профиля: {str(e)}')
        
        return render(request, 'users/edit_profile.html', {'user': user})
        
    except Users.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
        return redirect('authentication:login')
