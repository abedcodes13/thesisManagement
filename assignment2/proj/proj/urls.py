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

    path('register/supervisor/', views.register_supervisor, name='register_supervisor'),
    path('register/group/', views.register_group, name='register_group'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # path('add/supervisor/', views.add_supervisor, name='add supervisor'),
    # path('add/supervisor/done/', views.add_supervisor_submit),
    # re_path(r'^edit/supervisor/(?P<key>\w+)?/?$', views.modify_supervisor),
    # re_path(r'^delete/supervisor/(?P<key>\w+)?/?$', views.modify_supervisor),

    # path('group/new/', views.add_group, name='group_create'),
    # path('add/group/done/', views.add_group_submit),
    # re_path(r'^edit/group/(?P<key>\w+)?/?$', views.modify_group),
    # re_path(r'^delete/group/(?P<key>\w+)?/?$', views.modify_group),    

    path('topic/new/', views.add_topic, name='topic_create'),
    path('add/topic/done/', views.add_topic_submit),
    re_path(r'^edit/topic/(?P<key>\w+)?/?$', views.modify_topic),
    re_path(r'^delete/topic/(?P<key>\w+)?/?$', views.modify_topic),

    path('application/new/', views.add_application, name='application_create'),
    path('add/application/done/', views.add_application_submit),
    re_path(r'^edit/application/(?P<key>\w+)?/?$', views.modify_application),
    re_path(r'^delete/application/(?P<key>\w+)?/?$', views.modify_application),
]
