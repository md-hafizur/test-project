from django.db import models
from account.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'projects'
        
    def __str__(self):
        return self.name
    

class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Member', 'Member'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    
    class Meta:
        db_table = 'project_members'
        unique_together = ['project', 'user']
        
    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"
    