from django.db import models
from django.utils import timezone
from main.models.Register import Register

class UserLogin(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  
    ip_address = models.CharField(max_length=100)
    login_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.name} {self.user.surname} - {self.ip_address}"