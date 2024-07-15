from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Register
from main.forms import RegisterForm

def user_profile_detail_views(request, id):
    profil_entry = get_object_or_404(Register, id=id)
    form = RegisterForm(instance=profil_entry)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=profil_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil başarıyla güncellendi.')
            return redirect('users_list')

    return render(request, 'admin/usersprofile.html', {'form': form})
