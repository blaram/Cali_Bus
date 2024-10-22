from django.db import models
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL
# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    desc = models.CharField(max_length=500, null=True,
                            blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'Roles'
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        ordering = ['id']


class Bus(models.Model):
    plate = models.CharField(max_length=10, unique=True, verbose_name='Placa')
    brand = models.CharField(max_length=150, verbose_name='Marca')
    model = models.CharField(max_length=150, verbose_name='Modelo')
    capacity = models.IntegerField(verbose_name='Capacidad')
    image = models.ImageField(upload_to='bus/%Y/%m/%d', null=True, blank=True)
    year = models.IntegerField(verbose_name='Año')
    status = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.plate

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        db_table = 'Buses'
        verbose_name = 'bus'
        verbose_name_plural = 'buses'
        ordering = ['id']
