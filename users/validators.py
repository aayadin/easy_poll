from django import forms


def validate_not_empty(value):
    if value == '':
        raise forms.ValidationError(
            'Field cant be empty',
            params={'value': value},
        )
