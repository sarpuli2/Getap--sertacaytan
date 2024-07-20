from django.shortcuts import render
from django.http import JsonResponse
from main.models import TamamlananGorev

def admin_tamamlanan_gorev_views(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        gorev_id = data.get('gorev_id')
        if gorev_id:
            TamamlananGorev.objects.filter(id=gorev_id).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)

    tamamlanan_gorevler = TamamlananGorev.objects.select_related('gorev', 'user').all()
    return render(request, 'gorev/admintamamlanangorev.html', {'tamamlanan_gorevler': tamamlanan_gorevler})
