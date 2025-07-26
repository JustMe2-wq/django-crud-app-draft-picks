from django import forms
from .models import Draft
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DraftForm(forms.ModelForm):
    class Meta:
        model = Draft
        fields = ['pick', 'player']
        widgets = {
            'pick': forms.Select(
                attrs={
                    'placeholder': 'Select a pick',
                    'type': 'select',
                }
            ),
            'player': forms.Select(
                attrs={
                    'placeholder': 'Select a player',
                    'type': 'select',
                }
            ),
        }

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']