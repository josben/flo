
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User
from staff.models import Staff

class CoreUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'staff', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)
        return password2
   
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CoreUserCreationForm,
                        self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CoreUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the
        # initial value. This is done here, rather than on
        # the field, because the field does not have access
        # to the initial value
        return self.initial["password"]


class CoreUserAdmin(UserAdmin):
    add_form = CoreUserCreationForm
    form = CoreUserChangeForm
   
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser',
                         'is_active', 'groups')
    search_fields = ('email', 'username')
    ordering = ('email', 'username')
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields':
                                ('username', 'staff')}),
        ('Permissions', {'fields': ('is_active',
                                'is_staff',
                                'is_superuser',
                                'groups',
                                'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',
                        'password1', 'password2')}
        ),
    )

admin.site.unregister(User)
admin.site.register(User, CoreUserAdmin)

