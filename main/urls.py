from django.urls import path
from main.views import (
    anasayfa_view,
    login_view,
    register_view,
    profil_view,
    update_view,
    delete_view,
    users_views,
    user_detail_views,
    user_delete,
    activate,
    passwordchange
)
from main.views.nvbar_views.logout_view import logout_view
from main.views.nvbar_views.stajyerinfo_view import stajyerinfo_view
from main.views.user_views.sendpasswordkey_view import sendpasswordkey_view
from main.views.user_views.user_profile_detail_views import user_profile_detail_views
from main.views.gorev_views.admin_gorev_ver_views import admin_gorev_ver_views
from main.views.gorev_views.admin_tamamlanan_gorev_views import admin_tamamlanan_gorev_views
from main.views.gorev_views.kullanici_gorev_detay_views import gorev_detay_views
from main.views.gorev_views.kullanici_gorevler_views import gorevler_views
from main.views.gorev_views.kullanici_gorev_tamamla_views import gorev_tamamla_views 
from main.views.gorev_views import admin_tamamlanan_gorev_views
from main.views.siteLog.ipforadmin import ipforadmin_list, iplogsıfırla
from django.urls import path, include
from rest_framework.routers import DefaultRouter



from main.views.test_views import test_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [ 
    #test
    path('test/', test_view, name='test'),
    #main
    path('', anasayfa_view, name='anasayfa'),
    # kayıt-giriş
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    # nvbar
    path('anasayfa/', anasayfa_view, name='anasayfa'),
    path('stajyerinfo/', stajyerinfo_view, name='stajyerinfo'),
    path('profil/', profil_view, name='profil'),
    # crud
    path('update/<int:id>/', update_view, name='update'),
    path('delete/<int:id>/', delete_view, name='delete'),
    # şifre yenileme
    path('sendmail/', sendpasswordkey_view, name='sendmail'),
    # aktifleme tokenli
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('passwordchange/<uidb64>/<token>/', passwordchange, name='passwordchange'),
    # kullanıcı yönetim
    path('users/', users_views, name='users_list'),
    path('userdetail/<int:id>/', user_profile_detail_views, name='user_profile_detail'),
    path('users/<int:user_id>/', user_detail_views, name='user_detail'), 
    path('users/delete/<int:user_id>/', user_delete, name='user_delete'),
    # kullanıcı ve admin görev
    path('gorev/detay/<int:gorev_id>/', gorev_detay_views, name='gorev_detay'),
    path('gorev/tamamla/<int:gorev_id>/', gorev_tamamla_views, name='gorev_tamamla'),
    path('gorev_ver/', admin_gorev_ver_views, name='admin_gorev_ver'),
    path('tamamlanan-gorevler/', admin_tamamlanan_gorev_views, name='admin_tamamlanan_gorevler'),
    path('kullanicigorevler/<int:user_id>/', gorevler_views, name='kullanicigorevler'),
    #ip listeleme
    path('iplog/', ipforadmin_list, name='ipforadmin_list'),
    path('iplog/sıfırla/', iplogsıfırla, name='iplogsıfırla'),
    


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
