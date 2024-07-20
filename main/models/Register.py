from django.db import models
from django.utils import timezone

class Register(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to='media/')
    surname = models.CharField(max_length=50)
    mail = models.EmailField()
    password = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)
    aktifmi = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    yetki_choices = [
        ('User', 'User'),
        ('Admin', 'Admin'),
        ('Kurucu', 'Kurucu')
    ]
    yetki = models.CharField(max_length=20, choices=yetki_choices)
    hesapTarih = models.DateField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    completed_tasks = models.IntegerField(default=0) 

    def __str__(self):
        return f'{self.name} {self.surname}'
    
    @property
    def is_authenticated(self):
        return True
