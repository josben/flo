
from django import forms
from core.models import User
from notifications.models import Notification

class NotificationForm(forms.ModelForm):
    PRIORITY_CHOICES = (
        (1, 'Prioridad Alta'),
        (2, 'Prioridad Media'),
        (3, 'Prioridad Baja'),
    )

    priority = forms.ChoiceField(choices=PRIORITY_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control',
                                                            'autofocus': ''}))
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_admin=True).filter(is_superuser=False),
                                          widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Notification
        exclude = ['date_created']
        widgets = {
                'type_notification': forms.Select(attrs={'class': 'form-control'}),
                'abstract': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Descripcion corta',
                                                   'autocomplete': 'off'}),
                'description': forms.Textarea(attrs={'rows': '3',
                                                     'class': 'form-control',
                                                     'placeholder': 'Descripcion detallada'})
                }

class NotificationFromAdminForm(forms.ModelForm):
    PRIORITY_CHOICES = (
        (1, 'Prioridad Alta'),
        (2, 'Prioridad Media'),
        (3, 'Prioridad Baja'),
    )

    priority = forms.ChoiceField(choices=PRIORITY_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control',
                                                            'autofocus': ''}))
    owner = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=False).filter(id__gt=0),
                                          widget=forms.Select(attrs={'class': 'form-control'}),
                                  required=False)
    to_all = forms.BooleanField(required=False)
    only_guard = forms.BooleanField(required=False)

    class Meta:
        model = Notification
        exclude = ['date_created']
        widgets = {
                'type_notification': forms.Select(attrs={'class': 'form-control'}),
                'abstract': forms.TextInput(attrs={'class': 'form-control',
                                                   'placeholder': 'Descripcion corta',
                                                   'autocomplete': 'off'}),
                'description': forms.Textarea(attrs={'rows': '3',
                                                     'class': 'form-control',
                                                     'placeholder': 'Descripcion detallada'})
                }

    def clean(self):
        cleaned_data = self.cleaned_data
        owner = self.cleaned_data.get('owner')
        to_all = self.cleaned_data.get('to_all')
        only_guard = self.cleaned_data.get('only_guard')
        if not owner and not to_all and not only_guard:
            raise forms.ValidationError('Debe mandar a una persona o seleccionar' +
                                        ' la opcion de Enviar a todos')
        else:
            return cleaned_data

