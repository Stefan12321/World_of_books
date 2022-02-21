from django import forms
from django.core.exceptions import ValidationError
from .validators import validate_email, validate_username


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}),  validators=[validate_username])
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}), validators=[validate_email])
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        val_password = cleaned_data.get("password")
        val_confirm_password = cleaned_data.get("confirm_password")
        print(val_password, val_confirm_password)
        if val_password != val_confirm_password:
            raise ValidationError('Password does not match')