from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from project.models import Task
from rest_framework.permissions import IsAuthenticated
from authentication.auth import JWTAuthentication
from rest_framework.response import Response
class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer
    
    def get_queryset(self):
        task_id = self.kwargs.get('task_id')
        user = self.request.user
        
        # Check if user has access to the task
        task = Task.objects.filter(
            id=task_id,
            project__members__user=user
        ).first()
        
        if not task:
            return Comment.objects.none()
        
        return Comment.objects.filter(task=task).select_related('user')
    
    def perform_create(self, serializer):
        task_id = self.kwargs.get('task_id')
        serializer.save(user=self.request.user, task_id=task_id)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(
            task__project__members__user=user
        ).select_related('user', 'task')
    
    def update(self, request, *args, **kwargs):
        partial = True  # Force partial update even on PUT
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)