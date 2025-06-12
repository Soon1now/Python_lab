from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('authentication.urls', 'authentication'), namespace='authentication')),
    path('admin_panel/', include(('admin_panel.urls', 'admin_panel'), namespace='admin_panel')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('account/', include('users.urls')),
    path('', include(('main.urls', 'main'), namespace='main')),
    path('teacher/', include(('teacher_panel.urls', 'teacher_panel'), namespace='teacher_panel')),
]
