from django.shortcuts import render, redirect
from main.models import UserLogin
from django.contrib import messages

def ipforadmin_list(request):
    userlogins = UserLogin.objects.all()
    context = {
        'userlogins': userlogins
    }
    return render(request, 'siteLog/ipforadmin.html', context)

def iplogsıfırla(request):
    if request.method == 'POST':
        UserLogin.objects.all().delete()
        messages.success(request, 'IP logları başarıyla sıfırlandı.')
        return redirect('ipforadmin_list')
    return render(request, 'siteLog/ipforadmin.html')
