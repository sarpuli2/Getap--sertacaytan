from django.db import models

class SpecialDay(models.Model):
    is_special_day = models.BooleanField(default=False)
    last_checked = models.DateField(auto_now=True)
