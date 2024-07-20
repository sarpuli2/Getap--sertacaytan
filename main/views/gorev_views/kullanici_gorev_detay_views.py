from django.shortcuts import render, get_object_or_404
from main.models import VerilenGorev

def gorev_detay_views(request, gorev_id):
    gorev = get_object_or_404(VerilenGorev, id=gorev_id)
    return render(request, 'gorev/gorevdetay.html', {'gorev': gorev})
