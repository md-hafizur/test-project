# project/task_urls.py
from django.urls import path
from .views import TaskListCreateView

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),  # /api/projects/<project_pk>/tasks/
]
