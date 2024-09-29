from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True,
                            blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Roles'
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        ordering = ['id']
