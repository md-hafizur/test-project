"""
URL configuration for techforing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from comments.views import CommentDetailView
from project.views import TaskDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('account.urls')),
    path('api/projects/', include('project.urls')),
    path('api/projects/<int:project_pk>/tasks/', include('project.task_urls')),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('api/tasks/<int:task_id>/comments/', include('comments.urls')),
    path('api/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
