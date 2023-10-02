from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='Ваше имя')
    last_name = forms.CharField(required=True, label='Ваша фамилия')
    email = forms.EmailField(required=True, label='Ваш Email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        help_texts = {
            'username': 'Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
        }


class PasswordResetFormValidation(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "Пользователь с данным адресом электронной почты не существует."
            self.add_error('email', msg)
        return email
