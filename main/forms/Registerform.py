from django import forms
from main.models import Register

class RegisterForm(forms.ModelForm):   
    class Meta:
        model = Register
        fields = ['image', 'name', 'surname', 'mail', 'password', 'password2', 'yetki', 'aktifmi']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'yetki': forms.Select(choices=Register.yetki_choices, attrs={'class': 'form-control'}),
            'aktifmi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
