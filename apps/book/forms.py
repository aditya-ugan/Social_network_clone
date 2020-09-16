from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Train,Bus,Flight,TrainFare

class TrainSearch(forms.ModelForm):
    class Meta:
        model=Train
        fields=['source','destination','day']


class FlightSearch(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['source', 'destination', 'day']


class BusSearch(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['source', 'destination', 'day']


class TrainFareForm(forms.ModelForm):
    class Meta:
        model=TrainFare
        fields=['category']

class CreateUser(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']