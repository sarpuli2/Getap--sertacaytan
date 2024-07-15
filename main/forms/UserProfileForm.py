from django import forms
from main.models import Register
from django.utils import timezone

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['name', 'surname', 'mail', 'password', 'password2', 'aktifmi']
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['aktifmi']:
            instance.hesapTarih = timezone.now().date()
        if commit:
            instance.save()
        return instance
