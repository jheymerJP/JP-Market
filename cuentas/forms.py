from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'correo@ejemplo.com'}))
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'usuario'}))
    password1 = forms.CharField(label='Contrasena', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Minimo 8 caracteres'}))
    password2 = forms.CharField(label='Confirmar contrasena', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Repite tu contrasena'}))
    telefono = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '999 888 777'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contrasenas no coinciden')
        return p2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya esta en uso')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            UserProfile.objects.filter(user=user).update(
                telefono=self.cleaned_data.get('telefono', ''),
            )
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['telefono', 'direccion', 'ciudad', 'distrito', 'documento_tipo', 'documento_numero']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Av. La Marina 123'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Lima'}),
            'distrito': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'San Isidro'}),
            'telefono': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '999 888 777'}),
            'documento_numero': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '12345678'}),
        }
