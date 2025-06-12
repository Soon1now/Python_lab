from django.urls import path
from . import views

urlpatterns = [
    path('', views.courses, name='courses'),
    path('lesson/<int:lesson_id>/', views.lesson, name='lesson'),
    path('current/<int:course_id>/', views.current, name='current_course'),
    path('about/<int:course_id>/', views.about_course, name='about_course'),
] 