from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from django.core import exceptions
from rest_framework import serializers


def validate_password(password, user):
    errors = dict()
    try:
        django_validate_password(password=password, user=user)
    except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)

    if errors:
        raise serializers.ValidationError(errors)
