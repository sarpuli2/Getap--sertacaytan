from django.contrib import admin
from main.models.Stajyerinfo import *
from main.models.Register import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
# Register your models here.
admin.site.register(Stajyerinfo)
admin.site.register(Register)
