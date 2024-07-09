from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import Kullaniciveri
from .models import Register, Anasayfa
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Anasayfa 

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
                register = Register(name=name, surname=surname, mail=mail, password=password, password2=password2)
                register.save()
                messages.success(request, 'Kayıt Başarılı')
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
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_surname'] = user.surname
            request.session['user_mail'] = user.mail
            
            messages.success(request, 'Login successful')
            return redirect('anasayfa')
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
                bolum = form.cleaned_data['bolum']
                kacyillik = form.cleaned_data['kacyillik']
                tamamdevam = form.cleaned_data['tamamdevam']
                donem = form.cleaned_data['donem']
                biografi = form.cleaned_data['biografi']
                cinsiyet = form.cleaned_data['cinsiyet']
                telefon = form.cleaned_data['telefon']
                mail = form.cleaned_data['mail']
                aktif = form.cleaned_data['aktif']

                anasayfa_entry = Anasayfa(
                    user_id=user_id,
                    name=user_name,
                    bolum=bolum,
                    kacyillik=kacyillik,
                    tamamdevam=tamamdevam,
                    donem=donem,
                    biografi=biografi,
                    cinsiyet=cinsiyet,
                    telefon=telefon,
                    mail=mail,
                    aktif=aktif
                )
                anasayfa_entry.save()

                messages.success(request, 'İletişim bilgileri başarıyla kaydedildi.')
                return redirect('anasayfa')
            else:
                messages.error(request, 'Form geçerli değil: ' + str(form.errors))
        else:
            form = Kullaniciveri()

        return render(request, 'anasayfa.html', {'form': form, 'user_name': user_name, 'user_surname': user_surname})

def delete_view(request, id):
    obj = get_object_or_404(Anasayfa, id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('anasayfa')  
    return HttpResponse('Silme işlemi başarısız oldu.')

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

def logout_view(request):
    logout(request)
    return redirect('login')
