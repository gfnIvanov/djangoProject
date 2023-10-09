from django import forms
from django.core.exceptions import ValidationError


class RequiredField(forms.CharField):
    required = True
    default_error_messages = {'required': 'Поле обязательно для заполнения'}

class RegisterForm(forms.Form):
    user_login = RequiredField()
    user_password = RequiredField()
    password_confirm = RequiredField()
    password_confirm = RequiredField()
    user_firstname = RequiredField()
    user_surname = RequiredField()

    def clean(self):
        cleaned_data = super().clean()
        user_password = cleaned_data.get('user_password')
        password_confirm = cleaned_data.get('password_confirm')

        if user_password and password_confirm:
            if password_confirm != user_password:
                msg = ValidationError('Пароли не совпадают', code='mismatch')
                self.add_error('user_password', msg)
                self.add_error('password_confirm', msg)
            