from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Users, Students, Courses, Lessons, Teachers, RecordsStudents
import pandas as pd
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
import io
import re

def validate_password(password):
    if len(password) < 8:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'\d', password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True

def validate_name(name):
    if not name or len(name.strip()) < 2:
        return False, 'Имя и фамилия должны содержать минимум 2 символа'
    
    if not re.match(r'^[А-ЯЁA-Z][а-яА-ЯёЁa-zA-Z\s-]+$', name):
        return False, 'Имя и фамилия должны начинаться с заглавной буквы и содержать только буквы, пробелы и дефис'
    
    return True, ''

def main_page_admin(request):
    tab = request.GET.get('tab', 'students')
    students = Users.objects.filter(role='student')
    teachers = Users.objects.filter(role='teacher')
    admins = Users.objects.filter(role='admin')
    courses = Courses.objects.all()
    context = {
        'active_tab': tab,
        'students': students,
        'teachers': teachers,
        'admins': admins,
        'courses': courses,
    }
    return render(request, 'admin_panel/main_page_admin.html', context)

def add_user(request):
    if request.method == 'POST':
        role = request.POST.get('role')  
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([first_name, last_name, email]):
            messages.error(request, 'Пожалуйста, заполните все обязательные поля')
            return redirect('admin_panel:add_user') 

        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return redirect('admin_panel:add_user')


        is_valid_name = validate_name(first_name),
        is_valid_last_name = validate_name(last_name),
        name_error = validate_name(first_name) + validate_name(last_name)

        if not is_valid_name or not is_valid_last_name:
            messages.error(request, name_error)
            return redirect('admin_panel:add_user')
                
        if not validate_password(password):
            messages.error(request, 'Пароль не соответствует требованиям безопасности')
            return redirect('admin_panel:add_user')

        user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=role  
        )
        user.save()

        if role == 'student':
            student = Students(is_user=user)
            student.save()
        elif role == 'teacher':
            teacher = Teachers(id_user=user)
            teacher.save()
            
        messages.success(request, 'Пользователь успешно добавлен')
        return redirect('admin_panel:main_page_admin')
    
    return render(request, 'admin_panel/add_user.html')


def edit_user(request, user_id):
    user = get_object_or_404(Users, id_user=user_id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate name

        is_valid_name = validate_name(first_name),
        is_valid_last_name = validate_name(last_name),
        name_error = validate_name(first_name) + validate_name(last_name)

        if not is_valid_name or not is_valid_last_name:
            messages.error(request, name_error)
            return redirect('admin_panel:edit_user', user_id=user_id)

        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if password:
            if not validate_password(password):
                messages.error(request, 'Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, цифры и спецсимволы')
                return redirect('admin_panel:edit_user', user_id=user_id)
            user.password = password

        user.save()
        messages.success(request, 'Пользователь успешно обновлен')
        return redirect('admin_panel:main_page_admin')

    return render(request, 'admin_panel/edit_user.html', {'user': user})


def delete_user(request, user_id):
    user = get_object_or_404(Users, id_user=user_id)
    try:
        student = Students.objects.filter(is_user=user).first()
        if student:
            RecordsStudents.objects.filter(id_student=student).delete()
            student.delete()

        teacher = Teachers.objects.filter(id_user=user).first()
        if teacher:
            Courses.objects.filter(id_teacher=teacher).delete()
            teacher.delete()

        user.delete()
        messages.success(request, 'Пользователь успешно удален')
    except Exception as e:
        messages.error(request, f'Ошибка при удалении пользователя: {str(e)}')
    return redirect('admin_panel:main_page_admin')

def export_teachers_excel(request):
    teachers = Users.objects.filter(role='teacher').values('id_user', 'first_name', 'last_name', 'email', 'password')
    df = pd.DataFrame(list(teachers))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Teachers')
    output.seek(0)
    response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=teachers.xlsx'
    return response

def export_teachers_html(request):
    teachers = Users.objects.filter(role='teacher')
    html = render_to_string('admin_panel/export_teachers.html', {'teachers': teachers})
    response = HttpResponse(html, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename=teachers.html'
    return response
