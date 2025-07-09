from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectCreateSerializer, TaskSerializer, TaskCreateSerializer
from rest_framework.permissions import IsAuthenticated
from authentication.auth import JWTAuthentication
from project.models import Task

class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(members__user=user)
        ).distinct().prefetch_related('members__user')


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(members__user=user)
        ).distinct().prefetch_related('members__user')
    

class TaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            project_id = self.kwargs.get('project_pk')
            TaskCreateSerializer.context = {'project_id': project_id}
            return TaskCreateSerializer
        return TaskSerializer
    
    def get_queryset(self):
        project_id = self.kwargs.get('project_pk')
        user = self.request.user
        
        # Check if user has access to the project
        project = Project.objects.filter(
            id=project_id,
            members__user=user
        ).first()
        
        if not project:
            return Task.objects.none()
        
        return Task.objects.filter(project=project).select_related('assigned_to', 'project')
    
    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_pk')
        serializer.save(project_id=project_id)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            project__members__user=user
        ).select_related('assigned_to', 'project')
    

    def update(self, request, *args, **kwargs):
        partial = True  # Force partial update even on PUT
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)