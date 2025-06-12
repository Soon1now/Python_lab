from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('account/', views.account, name='account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
] 