from django.shortcuts import render
from main.models import Register, VerilenGorev

def gorevler_views(request, user_id):  
    user = Register.objects.get(id=user_id)
    tasks = VerilenGorev.objects.filter(assigned_to=user)

    return render(request, 'gorev/kullanicigorevler.html', {'tasks': tasks})

 