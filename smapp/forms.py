# -*- coding: utf-8 -*-
from django import forms
from smapp.models import *
from chosen import forms as chosenforms


def filtra(rut):
    """
    Esta funcion cumple el trabajo de filtrar el RUN.
    Omitiendo asi los puntos (.) y Guiones (-) y cualquier otro caracter
    que no incluya la variable 'caracteres'.
    """
    caracteres = "1234567890k"
    rutx = ""
    for cambio in rut.lower():
        if cambio in caracteres:
            rutx += cambio
    return rutx


def valida(rut):
    """
    Esta funcion cumple el trabajo de realizar la logica de negocio,
    ya sea matematica como logica.
    """
    rfiltro = filtra(rut)
    rutx = str(rfiltro[0:len(rfiltro)-1])
    digito = str(rfiltro[-1])
    multiplo = 2
    total = 0
    for reverso in reversed(rutx):
        total += int(reverso) * multiplo
        if multiplo == 7:
            multiplo = 2
        else:
            multiplo += 1
        modulus = total % 11
        verificador = 11 - modulus
        if verificador == 10:
            div = "k"
        elif verificador == 11:
            div = "0"
        else:
            if verificador < 10:
                div = verificador
    if str(div) == str(digito):
        retorno = "Valido"
    else:
        retorno = "Invalido"
    return retorno


class TakeNameField(chosenforms.ChosenModelChoiceField):
    def label_from_instance(self, obj):
        # return whatever text you want
        return 'Nombre: ' + obj.userOrigin.first_name + ' ' + obj.userOrigin.last_name + ' ' + 'Piso: ' + str(obj.apartment.floor) + ' ' + 'Numero: ' +str(obj.apartment.number)


class VisitForm(forms.ModelForm):

    name = forms.CharField(label='Nombre completo',
                           min_length=5,
                           widget=forms.TextInput,
                           )
    rut = forms.CharField(label='Rut',
                          widget=forms.TextInput,
                          max_length=12,
                          validators=[valida]
                          )

    resident = TakeNameField(queryset=Resident.objects.all())
    note = forms.CharField(label='Nota',
                           widget=forms.Textarea,
                           min_length=10,
                           required=False,
                           )
    received = forms.BooleanField(label='Recibido', required=False)

    class Meta:
        model = Visit
        fields = ('name', 'rut', 'resident', 'note', 'received')


class PublicationForm(forms.ModelForm):
    CHOICES = (('1', 'Evento'), ('2', 'Reunion'), ('3', 'Urgente'), ('4', 'Aviso'), ('5', 'Otro'))
    title = forms.CharField(label='Titulo', max_length=100)
    message = forms.TextInput()
    type = forms.ChoiceField(choices=CHOICES)

    class Meta:
        model = Publication
        fields = ('title', 'message', 'type')


class TakeLocationField(chosenforms.ChosenModelChoiceField):
    def label_from_instance(self, obj):
        # return whatever text you want
        return obj.name


class EventForm(forms.ModelForm):
    start = forms.CharField()
    location = TakeLocationField(queryset=Location.objects.all())

    class Meta:
        model = Event
        fields = ('start', 'location',)


class RentForm(forms.ModelForm):
    CHOICES = (('Enero', 'Enero'), ('Febrero', 'Febrero'), ('Marzo', 'Marzo'), ('Abril', 'Abril'), ('Mayo', 'Mayo'), ('Junio', 'Junio'), ('Julio', 'Julio'), ('Agosto', 'Agosto'), ('Septiembre', 'Septiembre'), ('Octubre', 'Octubre'), ('Noviembre', 'Noviembre'), ('Diciembre', 'Diciembre'))
    month = forms.ChoiceField(choices=CHOICES)
    amount = forms.IntegerField()
    resident = TakeNameField(queryset=Resident.objects.all())

    class Meta:
        model = Rent
        fields = ('month', 'amount', 'resident')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(label='Rut',
                               min_length=5,
                               widget=forms.TextInput,
                               )

    first_name = forms.CharField(label='Nombre',
                                 min_length=5,
                                 widget=forms.TextInput,
                                 )
    last_name = forms.CharField(label='Apellido',
                                min_length=5,
                                widget=forms.TextInput,
                                )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class TakeAparmentField(chosenforms.ChosenModelChoiceField):
    def label_from_instance(self, obj):
        # return whatever text you want
        return 'Nº: ' + str(obj.number) + ' ' + 'Piso: ' + str(obj.floor)


class ResidentForm(forms.ModelForm):
    phone = models.CharField(max_length=20)
    apartment = TakeAparmentField(queryset=Apartment.objects.all())

    class Meta:
        model = Resident
        fields = ('phone', 'apartment',)