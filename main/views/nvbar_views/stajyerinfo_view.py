from django.shortcuts import render, redirect
from main.models import Stajyerinfo, Register
from main.forms import Kullaniciveri
from django.contrib import messages

def stajyerinfo_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user_name = request.session.get('user_name')
    user_surname = request.session.get('user_surname')

    try:
        stajyerinfo_entry = Stajyerinfo.objects.get(register__id=user_id)
        return redirect('update', id=stajyerinfo_entry.register.id)
    except Stajyerinfo.DoesNotExist:
        if request.method == 'POST':
            form = Kullaniciveri(request.POST, request.FILES)
            if form.is_valid():
                stajyerinfo_entry = form.save(commit=False)
                stajyerinfo_entry.register = Register.objects.get(id=user_id)
                stajyerinfo_entry.name = user_name
                stajyerinfo_entry.save()
                messages.success(request, 'İletişim bilgileri başarıyla kaydedildi.')
                return redirect('stajyerinfo')
            else:
                messages.error(request, 'Form geçerli değil: ' + str(form.errors))
        else:
            form = Kullaniciveri()

        return render(request, 'nvbar/stajyerinfo.html', {'form': form, 'user_name': user_name, 'user_surname': user_surname})