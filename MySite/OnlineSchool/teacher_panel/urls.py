from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_dashboard, name='dashboard'),
    path('task/', views.task, name='task'),
]