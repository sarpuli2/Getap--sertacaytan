from main.models import Register
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        password = request.POST['password']
        
        user = Register.objects.filter(mail=mail, password=password).first()
        if user is not None:
            
            if (timezone.now().date() - user.hesapTarih).days > 30:
                user.aktifmi = False
                user.save()
                
            if user.aktifmi:
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_surname'] = user.surname
                request.session['user_mail'] = user.mail
                request.session['user_yetki'] = user.yetki
                request.session['is_authenticated'] = True
                
                messages.success(request, 'Giriş Başarılı!.')
                return redirect('anasayfa')
            else:
                messages.warning(request, 'Lütfen mailinizi onaylayınız!')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış!')
    
    return render(request, 'nvbar/login.html')
