from rest_framework import serializers
from .models import Project, ProjectMember, Task
from account.serializers import UserSerializer
from account.models import User
from rest_framework.exceptions import ValidationError

class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'user_id', 'role']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']

class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description']
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        project = Project.objects.create(**validated_data)

        members = self.context['request'].data.get('members', [])
        for member in members:
            user_id = member.get('user_id')
            role = member.get('role')

            if not User.objects.filter(id=user_id).exists():
                raise ValidationError(f"User with id {user_id} does not exist")

            ProjectMember.objects.create(
                user_id=user_id,
                project=project,
                role=role
            )


        # Add owner as admin member
        ProjectMember.objects.create(
            project=project,
            user=project.owner,
            role='Admin'
        )
        
        return project


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority', 
            'assigned_to', 'assigned_to_id', 'project', 'created_at', 'due_date'
        ]
        read_only_fields = ['id', 'created_at']

class TaskCreateSerializer(serializers.ModelSerializer):
    assigned_to_id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'assigned_to_id', 'due_date']