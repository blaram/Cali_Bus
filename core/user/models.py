from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    image = models.ImageField(
        upload_to='users/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    ci = models.CharField(max_length=10, null=True,
                          blank=True, verbose_name='Cédula de Identidad')
    phone = models.CharField(max_length=20, null=True,
                             blank=True, verbose_name='Teléfono')

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')
