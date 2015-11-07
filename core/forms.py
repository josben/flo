
from django import forms

class ChangePasswordUserForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Nuevo Password'}))

