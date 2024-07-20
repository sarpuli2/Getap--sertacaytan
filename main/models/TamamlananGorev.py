from django.db import models
from main.models import Register, VerilenGorev

class TamamlananGorev(models.Model):
    gorev = models.ForeignKey(VerilenGorev, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='completed_tasks/', null=True, blank=True)
    github_link = models.URLField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} {self.user.surname} - {self.gorev.taskname}"
