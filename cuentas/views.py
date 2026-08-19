from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, UserProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('tienda:home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('tienda:home')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = UserRegistrationForm()
    return render(request, 'cuentas/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('tienda:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido de vuelta, {user.username}!')
            next_url = request.GET.get('next', 'tienda:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'cuentas/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente.')
    return redirect('tienda:home')


@login_required
def profile_view(request):
    return render(request, 'cuentas/profile.html')


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('cuentas:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'cuentas/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
