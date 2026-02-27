"""
URL configuration for ocms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # ── API endpoints ──
    path('api/auth/',        include('accounts.urls')),
    path('api/courses/',     include('courses.urls')),
    path('api/enrollments/', include('enrollments.urls')),
    path('api/reviews/',     include('reviews.urls')),

    # ── HTML Page URLs ──
    path('',                         views.login_page,           name='home'),
    path('auth/login/',              views.login_page,           name='login_page'),
    path('dashboard/',               views.student_dashboard,    name='student_dashboard'),
    path('my-courses/',              views.my_courses,           name='my_courses'),
    path('courses/',                 views.course_list,          name='course_list'),
    path('courses/<int:course_id>/', views.course_detail,        name='course_detail'),
    path('instructor/',              views.instructor_dashboard, name='instructor_dashboard'),
    path('admin-dashboard/',         views.admin_dashboard,      name='admin_dashboard'),
    path('auth/logout/', views.logout_page, name='logout'),
]
