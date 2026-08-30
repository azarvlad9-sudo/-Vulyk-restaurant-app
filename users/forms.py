from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary',
        'placeholder': 'Пароль'
    }), label="Пароль")

    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary',
        'placeholder': 'Підтвердіть пароль'
    }), label="Підтвердження пароля")

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Ім\'я користувача',
            'email': 'Email адреса',
        }
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'Логін'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Паролі не збігаються!")
        return cleaned_data