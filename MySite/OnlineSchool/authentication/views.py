from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re
from main.models import Users
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import secrets
import datetime


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

def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return redirect('authentication:registration')

        is_valid_name = validate_name(first_name),
        is_valid_last_name = validate_name(last_name),
        name_error = validate_name(first_name) + validate_name(last_name)

        if not is_valid_name or not is_valid_last_name:
            messages.error(request, name_error)
            return redirect('authentication:registration')

        if not validate_password(password):
            messages.error(request, 'Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, цифры и специальные символы')
            return redirect('authentication:registration')

        try:
            user = Users.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                role='student'
            )
            messages.success(request, 'Регистрация успешно завершена')
            return redirect('authentication:login')
        except Exception as e:
            messages.error(request, f'Ошибка при создании пользователя: {str(e)}')
            return redirect('authentication:registration')

    return render(request, 'auth/registration.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = Users.objects.get(email=email)
            if user.check_password(password):
                # Устанавливаем сессию
                request.session['user_id'] = user.id_user
                request.session['user_role'] = user.role
                request.session['user_email'] = user.email
                request.session['user_name'] = f"{user.first_name} {user.last_name}"
                
                # Перенаправляем на соответствующую страницу
                if user.role == 'student':
                    return redirect('users:account')
                elif user.role == 'teacher':
                    return redirect('teacher_panel:dashboard')
                else:
                    return redirect('admin_panel:main_page_admin')
            else:
                messages.error(request, 'Неверный пароль')
        except Users.DoesNotExist:
            messages.error(request, 'Пользователь не найден')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    request.session.flush()
    return redirect('authentication:login')

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Users.objects.get(email=email)
            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.reset_token_created = datetime.datetime.now()
            user.save()

            reset_url = request.build_absolute_uri(f'/auth/password-reset-confirm/{token}/')
            send_mail(
                'Восстановление пароля',
                f'Для восстановления пароля перейдите по ссылке: {reset_url}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Инструкции по восстановлению пароля отправлены на ваш email')
            return redirect('authentication:login')
        except Users.DoesNotExist:
            messages.error(request, 'Пользователь с таким email не найден')
    
    return render(request, 'auth/password_reset.html')

def password_reset_confirm(request, token):
    try:
        user = Users.objects.get(reset_token=token)
        # Проверяем, не истек ли срок действия токена (24 часа)
        if (datetime.datetime.now() - user.reset_token_created).total_seconds() > 86400:
            messages.error(request, 'Срок действия ссылки истек')
            return redirect('authentication:password_reset')
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            if validate_password(new_password):
                user.password = make_password(new_password)
                user.reset_token = None
                user.reset_token_created = None
                user.save()
                messages.success(request, 'Пароль успешно изменен')
                return redirect('authentication:login')
            else:
                messages.error(request, 'Пароль должен содержать минимум 8 символов, включая заглавные и строчные буквы, цифры и специальные символы')
        
        return render(request, 'auth/password_reset_confirm.html')
    except Users.DoesNotExist:
        messages.error(request, 'Недействительная ссылка для восстановления пароля')
        return redirect('authentication:password_reset')