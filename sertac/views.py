from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Register, Anasayfa
from .forms import Kullaniciveri
from .tokens import hesaponaytoken

def email_gonderme(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Hesap Aktivasyonu'
    message = render_to_string('email_gonderme.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': hesaponaytoken.make_token(user),
    })
    send_mail(
        mail_subject,
        message,
        'admin@example.com',
        [user.mail],
        fail_silently=False,
    )

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Register.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Register.DoesNotExist):
        user = None

    if user is not None and hesaponaytoken.check_token(user, token):
        user.aktifmi = True
        user.save()
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        request.session['user_surname'] = user.surname
        request.session['user_mail'] = user.mail
        return redirect('anasayfa')
    else:
        return render(request, 'login.html', {'warning': 'Lütfen Emailinizi doğrulayın.'})

def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        mail = request.POST['mail']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if Register.objects.filter(mail=mail).exists():
                messages.error(request, 'Böyle bir Email zaten var.')
            else:
                register = Register(name=name, surname=surname, mail=mail, password=password, password2=password2, aktifmi=False)
                register.save()
                messages.success(request, 'Kayıt Başarılı! Hesabınızı onaylamak için Emailinize gelen bağlantıya tıklayınız.')
                email_gonderme(register, request)
                return redirect('login')
        else:
            messages.error(request, 'Şifreler eşleşmiyor!')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        password = request.POST['password']
        
        user = Register.objects.filter(mail=mail, password=password).first()
        if user is not None:
            if user.aktifmi:
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_surname'] = user.surname
                request.session['user_mail'] = user.mail
                messages.success(request, 'Giriş Başarılı!.')
                return redirect('anasayfa')
            else:
                messages.warning(request, 'Lütfen mailinizi onaylayınız!')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre yanlış!')
    
    return render(request, 'login.html')

def anasayfa_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user_name = request.session.get('user_name')
    user_surname = request.session.get('user_surname')

    try:
        anasayfa_entry = Anasayfa.objects.get(user_id=user_id)
        return redirect('update', id=anasayfa_entry.id)
    except Anasayfa.DoesNotExist:
        if request.method == 'POST':
            form = Kullaniciveri(request.POST)
            if form.is_valid():
                anasayfa_entry = form.save(commit=False)
                anasayfa_entry.user_id = user_id
                anasayfa_entry.name = user_name
                anasayfa_entry.save()
                messages.success(request, 'İletişim bilgileri başarıyla kaydedildi.')
                return redirect('anasayfa')
            else:
                messages.error(request, 'Form geçerli değil: ' + str(form.errors))
        else:
            form = Kullaniciveri()

        return render(request, 'anasayfa.html', {'form': form, 'user_name': user_name, 'user_surname': user_surname})

def update_view(request, id):
    anasayfa_entry = get_object_or_404(Anasayfa, id=id)
    if request.method == 'POST':
        if 'update' in request.POST:
            form = Kullaniciveri(request.POST, instance=anasayfa_entry)
            if form.is_valid():
                form.save()
                messages.success(request, 'Veri başarıyla güncellendi.')
                return redirect('anasayfa')
        elif 'delete' in request.POST:
            anasayfa_entry.delete()
            messages.success(request, 'Veri başarıyla silindi.')
            return redirect('anasayfa')
    else:
        form = Kullaniciveri(instance=anasayfa_entry)

    return render(request, 'update.html', {'form': form})

def delete_view(request, id):
    obj = get_object_or_404(Anasayfa, id=id)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Veri başarıyla silindi.')
        return redirect('anasayfa')
    return HttpResponse('Silme işlemi başarısız oldu.')

def logout_view(request):
    logout(request)
    return redirect('login')
