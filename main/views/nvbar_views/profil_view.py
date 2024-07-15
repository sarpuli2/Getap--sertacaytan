from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.models import Register
from main.forms import RegisterForm

def profil_view(request):
    user_id = request.session.get('user_id')
    profil_entry = get_object_or_404(Register, id=user_id)
    form = RegisterForm(instance=profil_entry)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=profil_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veri başarıyla güncellendi.')
            return redirect('profil')

    return render(request, 'nvbar/profil.html', {'form': form})