from main.forms import Kullaniciveri
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Stajyerinfo
from django.contrib import messages

def update_view(request, id):
    stajyerinfo_entry = get_object_or_404(Stajyerinfo, register__id=id)
    form = Kullaniciveri(instance=stajyerinfo_entry)
    
    if request.method == 'POST':
        form = Kullaniciveri(request.POST, request.FILES, instance=stajyerinfo_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veri başarıyla güncellendi.')
            return redirect('stajyerinfo')

    return render(request, 'crud/update.html', {'form': form})