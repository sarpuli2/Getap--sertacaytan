# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from main.models import Stajyerinfo

class Kullaniciveri(forms.ModelForm):
    class Meta:
        model = Stajyerinfo
        fields = ['bolum', 'dal', 'kacyillik', 'tamamdevam', 'donem', 'biografi', 'cinsiyet', 'telefon', 'mail', 'aktif']

    def __init__(self, *args, **kwargs):
        super(Kullaniciveri, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Gönder', css_class='btn btn-primary'))


