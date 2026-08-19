from django.urls import path
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.profile_view, name='profile'),
    path('perfil/editar/', views.edit_profile_view, name='edit_profile'),
]
