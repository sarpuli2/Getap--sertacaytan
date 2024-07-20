from django.db import models
from main.models import Register

class VerilenGorev(models.Model):
    taskname = models.CharField(max_length=100)
    taskcontent = models.TextField()
    taskimage = models.ImageField(upload_to='tasks/', null=True, blank=True)
    taskfile = models.FileField(upload_to='tasks/', null=True, blank=True)
    assigned_by = models.ForeignKey(Register, related_name='assigned_tasks', on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(Register, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.taskname
