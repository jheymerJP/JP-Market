from django import forms
from .models import Cupon, Banner


class CuponForm(forms.ModelForm):
    class Meta:
        model = Cupon
        fields = ['codigo', 'descuento', 'uso_maximo', 'minimo_compra', 'expira', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['titulo', 'subtitulo', 'imagen', 'url_destino', 'activo', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
