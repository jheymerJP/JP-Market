from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from allauth.socialaccount.models import SocialApp
from .forms import UserRegistrationForm, UserUpdateForm, UserProfileForm
from .models import UserProfile
from carrito.models import Order


def google_login(request):
    try:
        SocialApp.objects.get(provider='google')
        return redirect('socialaccount_login')
    except SocialApp.DoesNotExist:
        messages.error(request, 'Google login no esta configurado. Contacta al administrador.')
        return redirect('cuentas:login')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('panel_admin:dashboard')
        return redirect('tienda:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}!')
            if user.is_staff:
                return redirect('panel_admin:dashboard')
            return redirect('tienda:home')
        else:
            messages.error(request, 'Usuario o contrasena incorrectos')
    else:
        form = AuthenticationForm()

    return render(request, 'cuentas/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('tienda:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente!')
            return redirect('tienda:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'cuentas/register.html', {'form': form})


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')[:10]
    return render(request, 'cuentas/profile.html', {
        'orders': orders,
        'profile': request.user.profile,
    })


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Perfil actualizado!')
            return redirect('cuentas:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)

    return render(request, 'cuentas/edit_profile.html', {
        'u_form': u_form,
        'p_form': p_form,
    })


@login_required
def order_tracking_view(request, order_id):
    order = Order.objects.filter(order_id=order_id, user=request.user).first()
    if not order:
        messages.error(request, 'Pedido no encontrado')
        return redirect('cuentas:profile')
    return render(request, 'cuentas/order_tracking.html', {'order': order})
