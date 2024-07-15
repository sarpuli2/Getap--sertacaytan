from django.shortcuts import render
from main.models import Register

def users_views(request):
    users = Register.objects.all()  # Fetch all users
    return render(request, 'admin/users.html', {'users': users})