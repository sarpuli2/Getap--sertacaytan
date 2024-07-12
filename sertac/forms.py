# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Stajyerinfo, Register

class Kullaniciveri(forms.ModelForm):
    class Meta:
        model = Stajyerinfo
        fields = ['image','bolum', 'dal', 'kacyillik', 'tamamdevam', 'donem', 'biografi', 'cinsiyet', 'telefon', 'mail', 'aktif']

    def __init__(self, *args, **kwargs):
        super(Kullaniciveri, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Gönder', css_class='btn btn-primary'))

class Kullaniciveri(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['name', 'surname', 'mail', 'password', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
