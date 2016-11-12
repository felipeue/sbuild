from django import forms
from smapp.models import Visit, UserSM
from datetime import date
from django.forms.extras.widgets import SelectDateWidget


class VisitForm(forms.ModelForm):
    name = forms.CharField(label='Nombre completo',
                           min_length=5,
                           widget=forms.TextInput,
                           )
    rut = forms.CharField(label='Rut',
                          widget=forms.TextInput,
                          min_length=10,
                          )
    resident = forms.ModelChoiceField(queryset=UserSM.objects.filter(user_type='R'))
    note = forms.CharField(label='Nota',
                           widget=forms.Textarea,
                           min_length=10,
                           )
    received = forms.BooleanField(label='Recibido')

    class Meta:
        model = Visit
        fields = ('name', 'rut', 'resident', 'note', 'received')