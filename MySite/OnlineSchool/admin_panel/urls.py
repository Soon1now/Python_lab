from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_admin, name='main_page_admin'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('export_teachers_excel/', views.export_teachers_excel, name='export_teachers_excel'),
    path('export_teachers_html/', views.export_teachers_html, name='export_teachers_html'),
] 