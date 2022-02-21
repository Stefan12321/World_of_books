from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_email(value):
    try:
        User.objects.get(email=value)
        raise ValidationError('This email is already used')
    except User.DoesNotExist:
        pass


def validate_username(value):
    try:
        User.objects.get(username=value)
        raise ValidationError('This username is already used')
    except User.DoesNotExist:
        pass
