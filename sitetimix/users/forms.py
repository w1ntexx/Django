from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-input"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-input"})
    )
    
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class RegisterUserForm(UserCreationForm):
    style_text = forms.TextInput(attrs={"class": "form-input"})
    style_password = forms.PasswordInput(attrs={"class": "form-input"})
    
    username = forms.CharField(
        label="Логин",
        widget=style_text,
        )
    password1 = forms.CharField(
        label="Пароль",
        widget=style_password,
        ) 
    password2 = forms.CharField(
        label="Повтор Пароля",
        widget=style_password,
        )
    
    
    class Meta:
        style_text = forms.TextInput(attrs={"class": "form-input"})
        style_password = forms.PasswordInput(attrs={"class": "form-input"})
                    
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2"
            ]
        labels = {
            "email": "E-mail",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }
        widgets = {
            "email": style_text,
            "first_name": style_text,
            "last_name": style_text,
        }

        
        def clean_email(self):
            email = self.clean_data["email"]
            if get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError("Такой E-mail уже существует")
            return email


class ProfileUserForm(forms.ModelForm):
    style_text = forms.TextInput(attrs={'class': 'form-input'})
    
    username = forms.CharField(
        disabled=True,
        label="Логин",
        widget=style_text,
        )
    email = forms.CharField(
        disabled=True,
        label="E-mail",
        widget=style_text,
        )
    
    class Meta:
        style_text = forms.TextInput(attrs={'class': 'form-input'})
        
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
        }
        widgets = {
            'first_name': style_text,
            'last_name': style_text,
        }

class UserPasswordChangeForm(PasswordChangeForm):
    style_password = forms.PasswordInput(attrs={"class": "form-input"})
    
    old_password = forms.CharField(
        label="Старый пароль",
        widget=style_password,
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=style_password,
    )
    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=style_password,
    )
    