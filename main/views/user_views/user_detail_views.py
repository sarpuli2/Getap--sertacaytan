from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Register, Stajyerinfo
from main.forms import Kullaniciveri

def user_detail_views(request, user_id):
    logged_user_id = request.session.get('user_id')
    if not logged_user_id:
        return redirect('login')

    user_name = request.session.get('user_name')
    user_surname = request.session.get('user_surname')

    try:
        stajyerinfo_entry = Stajyerinfo.objects.get(register__id=user_id)
    except Stajyerinfo.DoesNotExist:
        stajyerinfo_entry = None

    if request.method == 'POST':
        form = Kullaniciveri(request.POST, request.FILES, instance=stajyerinfo_entry)
        if form.is_valid():
            stajyerinfo_entry = form.save(commit=False)
            stajyerinfo_entry.register = get_object_or_404(Register, id=user_id)
            stajyerinfo_entry.name = user_name
            stajyerinfo_entry.save()
            messages.success(request, 'İletişim bilgileri başarıyla güncellendi.')
            return redirect('user_detail', user_id=user_id)  # Burada 'user_detail' URL adını kullanın
        else:
            messages.error(request, 'Form geçerli değil: ' + str(form.errors))
    else:
        form = Kullaniciveri(instance=stajyerinfo_entry)

    return render(request, 'admin/usersdetail.html', {'form': form, 'user_name': user_name, 'user_surname': user_surname})
