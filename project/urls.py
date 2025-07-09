from django.urls import path, include
from .views import ProjectListCreateView, ProjectDetailView

urlpatterns = [
    path('', ProjectListCreateView.as_view(), name='project-list-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('api/tasks/<int:task_id>/comments/', include('comments.urls'))
]