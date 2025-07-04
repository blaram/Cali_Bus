from django import forms
from core.user.models import User


class ResetPasswordForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese su nombre de usuario",
                "class": "form-control",
                "autocomplete": "off",
            }
        )
    )

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned.get("username")).exists():
            self._errors["error"] = self.errors.get("error", self.error_class())
            self._errors["error"].append(
                "El nombre de usuario ingresado no existe. Por favor, verifique e intente nuevamente."
            )
            # raise forms.ValidationError(
            #     "El nombre de usuario ingresado no existe. Por favor, verifique e intente nuevamente."
            # )
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get("username")
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Ingrese su contraseña",
                "class": "form-control",
                "autocomplete": "off",
            }
        )
    )

    confirmPassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repita la contraseña",
                "class": "form-control",
                "autocomplete": "off",
            }
        )
    )

    def clean(self):
        cleaned = super().clean()
        password = cleaned["password"]
        confirm_password = cleaned["confirmPassword"]
        if password != confirm_password:

            self._errors["error"] = self.errors.get("error", self.error_class())
            self._errors["error"].append("Las contraseñas deben ser iguales.")
            # raise forms.ValidationError(
            #     "El nombre de usuario ingresado no existe. Por favor, verifique e intente nuevamente."
            # )
        return cleaned
