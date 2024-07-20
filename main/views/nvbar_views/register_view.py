from main.models import Register
from django.contrib import messages
from django.shortcuts import render, redirect
from main.tasks import email_gonderme
from main.views.user_views.email_gonderme_aktivasyonıcın import email_gonderme

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        mail = request.POST.get('mail')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # User < Admin < Kurucu
        yetki = 'User'
        
        
        if password == password2:
            if Register.objects.filter(mail=mail).exists():
                messages.error(request, 'Böyle bir Email zaten var.')
            else:
                register = Register(name=name, surname=surname, mail=mail, password=password, password2=password2, aktifmi=False, yetki=yetki)
                register.save()
                messages.success(request, 'Kayıt Başarılı! Hesabınızı onaylamak için Emailinize gelen bağlantıya tıklayınız.')
                
                email_gonderme(register, request) 
                
                return redirect('login')
        else:
            messages.error(request, 'Şifreler eşleşmiyor!')
    
    return render(request, 'nvbar/register.html')
