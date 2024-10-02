from django.db import models
from django.forms import model_to_dict

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
