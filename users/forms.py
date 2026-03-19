from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=False, help_text="Optional. Input Your Phone Number."
    )
    username = forms.CharField(max_length=50, required=True)
    usable_password = None

    #  Чтобы отключить вывод
    #   Password-based authentication:
    #   Enabled
    #   Disabled
    #   Whether the user will be able to authenticate using a password or not, if disabled, they may stiil be able to
    #   authenticate using other backends, such as Single Sign-On or LDAP

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone Number must be an integer.")
        return phone_number
