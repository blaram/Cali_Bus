from crum import get_current_user
from django.db import models
from datetime import datetime

from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.calibus.choices import gender_choices
from core.models import BaseModel


class Route(BaseModel):
    origin = models.CharField(
        max_length=100, verbose_name='Origen')
    destination = models.CharField(
        max_length=500, null=True, blank=True, verbose_name='Destino')
    estimated_time = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='Tiempo estimado')

    def __str__(self):
        return self.origin

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Route, self).save()

    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_updated'])
        return item

    class Meta:
        db_table = 'Rutas'
        verbose_name = 'Ruta'
        verbose_name_plural = 'Rutas'
        ordering = ['id']


class Travel(models.Model):
    rou = models.ForeignKey(
        Route, on_delete=models.CASCADE, verbose_name='Ruta')
    departure = models.DateField(
        default=datetime.now, verbose_name='Fecha de salida')
    arrival = models.DateField(
        default=datetime.now, verbose_name='Fecha de llegada')
    status = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.departure

    def toJSON(self):
        item = model_to_dict(self)
        item['rou'] = self.rou.toJSON()
        return item

    class Meta:
        db_table = 'Viajes'
        verbose_name = 'Viaje'
        verbose_name_plural = 'Viajes'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    ci = models.CharField(max_length=10, unique=True,
                          verbose_name='Cédula de Identidad')
    phone = models.CharField(max_length=10, verbose_name='Teléfono')
    email = models.CharField(max_length=100, verbose_name='Correo electrónico')
    gender = models.CharField(
        max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        return item

    class Meta:
        db_table = 'Clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Parcel(models.Model):
    senderID = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='sent_parcels')
    receiverID = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='received_parcels')
    description = models.TextField(
        null=True, blank=True, verbose_name='Descripción')
    weight = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name='Peso')
    declare_value = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name='Valor declarado')
    shipping_cost = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name='Costo de envío')
    status = models.BooleanField(default=True, verbose_name='Estado')

    def __str__(self):
        return self.senderID.names

    class Meta:
        db_table = 'Encomiendas'
        verbose_name = 'Encomienda'
        verbose_name_plural = 'Encomiendas'
        ordering = ['id']


class ReceiptDetail(models.Model):
    parc = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    mount = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name='Monto')

    def __str__(self):
        return self.parc.description

    class Meta:
        db_table = 'DetallesRecibos'
        verbose_name = 'Detalle de Recibo'
        verbose_name_plural = 'Detalles de Recibos'
        ordering = ['id']
