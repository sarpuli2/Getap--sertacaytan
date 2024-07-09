from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
# Register your models here.
admin.site.register(Anasayfa)
admin.site.register(Register)
