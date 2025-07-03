from django import forms

from core.user.models import User


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["autofocus"] = True

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "ci",
            "phone",
            "email",
            "username",
            "password",
            "image",
            "groups",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese sus nombres",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese sus apellidos",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese su correo electrónico",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese tu nombre de usuario",
                }
            ),
            "password": forms.PasswordInput(
                render_value=True,
                attrs={
                    "placeholder": "Ingrese un password",
                },
            ),
            "groups": forms.SelectMultiple(
                attrs={
                    "class": "form-control select2",
                    "style": "width: 100%;",
                    "mltiple": "multiple",
                }
            ),
        }
        exclude = [
            "user_permissions",
            "last_login",
            "date_joined",
            "is_superuser",
            "is_staff",
            "is_active",
        ]

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data["password"]
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data["groups"]:
                    u.groups.add(g)
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["autofocus"] = True

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "ci",
            "phone",
            "email",
            "username",
            "password",
            "image",
        )
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese sus nombres",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese sus apellidos",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese su correo electrónico",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese tu nombre de usuario",
                }
            ),
            "password": forms.PasswordInput(
                render_value=True,
                attrs={
                    "placeholder": "Ingrese un password",
                },
            ),
        }
        exclude = [
            "user_permissions",
            "last_login",
            "date_joined",
            "is_superuser",
            "is_staff",
            "is_active",
            "groups",
        ]

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data["password"]
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data["error"] = form.errors
        except Exception as e:
            data["error"] = str(e)
        return data
