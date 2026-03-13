"""
URL configuration for proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path, include
from proj_app import views

urlpatterns = [    
    path('admin/', admin.site.urls),
    path('', views.home, name='homepage'),
    path('about/', views.about, name='about'),
    
    path('register/unit_coordinator/', views.register_unit_coordinator, name='register_unit_coordinator'),
    path('register/supervisor/', views.register_supervisor, name='register_supervisor'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/group/', views.register_group, name='register_group'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('register/topic/', views.add_topic, name='topic_create'),
    path('topics/edit/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('topics/', views.list_topics, name='list_topics'),
    path('topics/request_removal/<int:topic_id>/', views.request_removal, name='request_removal'),
    path('topics/review/', views.review_topics, name='review_topics'),
    path('topics/apply/<int:topic_id>/', views.apply_for_topic, name='apply_for_topic'),
    path('topics/approve/<int:topic_id>/', views.approve_topic, name='approve_topic'),
    path('topics/reject/<int:topic_id>/', views.reject_topic, name='reject_topic'),
    path('topics/list_removal_requests/', views.list_removal_requests, name='list_removal_requests'),
    path('topics/approve_removal/<int:topic_id>/', views.approve_removal, name='approve_removal'),
    path('topics/reject_removal/<int:topic_id>/', views.reject_removal, name='reject_removal'),
    path('topic/<int:topic_id>/', views.view_topic, name='view_topic'),
    path('topics/pending/', views.list_pending_topics, name='list_pending_topics'),
    path('topics/delete/<int:topic_id>/', views.delete_topic, name='delete_topic'),  #kept for future implementation
    path('topics/approve_changes/<int:topic_id>/', views.approve_topic_changes, name='approve_topic_changes'),
    path('topics/reject_changes/<int:topic_id>/', views.reject_topic_changes, name='reject_topic_changes'),
    
    path('groups/', views.list_groups, name='list_groups'),
    path('groups/enroll/<int:group_id>/', views.enroll_in_group, name='enroll_in_group'),
    
    path('applications/', views.list_applications, name='list_applications'),
    path('applications/approve/<int:application_id>/', views.approve_application, name='approve_application'),
    path('applications/reject/<int:application_id>/', views.reject_application, name='reject_application'),    
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),



]