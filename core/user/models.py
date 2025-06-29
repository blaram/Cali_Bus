from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    image = models.ImageField(
        upload_to="users/%Y/%m/%d", null=True, blank=True, verbose_name="Imagen"
    )
    ci = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="Cédula de Identidad"
    )
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Teléfono"
    )

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL, "img/empty.png")

    def toJSON(self):
        item = model_to_dict(
            self, exclude=["password", "groups", "user_permissions", "last_login"]
        )
        item["last_login"] = (
            self.last_login.strftime("%d-%m-%Y") if self.last_login else ""
        )
        item["date_joined"] = (
            self.date_joined.strftime("%d-%m-%Y") if self.date_joined else ""
        )
        item["image"] = self.get_image()
        return item

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.set_password(self.password)
        super().save(*args, **kwargs)
