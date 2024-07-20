from django.db import models
from django.utils import timezone 
from main.models.Register import Register

class Stajyerinfo(models.Model):
    register = models.OneToOneField(Register, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)
    bolum = models.CharField(max_length=50)
    dal_choices = [
        ('Front-End', 'Front-End'),
        ('Back-End', 'Back-End')
    ]
    dal = models.CharField(max_length=20, choices=dal_choices)
    kacyillik_choices = [
        ('lisans', 'Lisans (4 yıl)'),
        ('onlisans', 'Önlisans (2 yıl)')
    ]
    kacyillik = models.CharField(max_length=20, choices=kacyillik_choices)
    tamamdevam_choices = [
        ('tamam', 'Tamamladı'),
        ('devam', 'Okuyor')
    ]
    tamamdevam = models.CharField(max_length=20, choices=tamamdevam_choices)
    donem_choices = [
        ('uzun', 'Uzun dönem'),
        ('kisa', 'Kısa dönem')
    ]
    donem = models.CharField(max_length=20, choices=donem_choices)
    biografi = models.TextField()
    cinsiyet_choices = [
        ('erkek', 'Erkek'),
        ('kiz', 'Kız')
    ]
    cinsiyet = models.CharField(max_length=10, choices=cinsiyet_choices)
    telefon = models.CharField(max_length=15)
    mail = models.EmailField()
    aktif = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name