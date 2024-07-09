from django.urls import path
from .views import register_view, login_view, anasayfa_view
from . import views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('anasayfa/', anasayfa_view, name='anasayfa'),
    path('update/<int:id>/', views.update_view, name='update'),
    path('delete/<int:id>/', views.delete_view, name='delete'),
    path('logout/', views.logout_view, name='logout'),
]
