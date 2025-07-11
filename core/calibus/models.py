from crum import get_current_user
from django.db import models
from datetime import datetime

from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.calibus.choices import (
    gender_choices,
    parcel_choices,
    remittance_choices,
    travel_status_choices,
    ticket_type_choices,
    cashbox_type_choices,
    payment_method_choices,
    movement_type_choices,
    cashbox_status_choices,
)
from core.models import BaseModel

# Define una función para obtener la hora actual


def current_time():
    return datetime.now().time()


class Route(BaseModel):
    origin = models.CharField(max_length=100, verbose_name="Origen")
    destination = models.CharField(
        max_length=500, null=True, blank=True, verbose_name="Destino"
    )
    estimated_time = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Tiempo estimado"
    )

    def __str__(self):
        return self.origin

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Route, self).save()

    def toJSON(self):
        item = model_to_dict(self, exclude=["user_creation", "user_updated"])
        return item

    class Meta:
        db_table = "Rutas"
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"
        ordering = ["id"]


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name="Nombres")
    surnames = models.CharField(max_length=150, verbose_name="Apellidos")
    ci = models.CharField(
        max_length=10, unique=True, verbose_name="Cédula de Identidad"
    )
    nationality = models.CharField(
        max_length=20, default="Desconocido", verbose_name="Nacionalidad"
    )
    date_of_birth = models.DateField(
        default=datetime.now, verbose_name="Fecha de nacimiento"
    )
    phone = models.CharField(max_length=10, verbose_name="Teléfono")
    email = models.CharField(max_length=100, verbose_name="Correo electrónico")
    gender = models.CharField(
        max_length=10, choices=gender_choices, default="male", verbose_name="Sexo"
    )

    def __str__(self):
        return f"{self.names} {self.surnames}"

    def toJSON(self):
        item = model_to_dict(self)
        item["gender"] = {"id": self.gender, "name": self.get_gender_display()}
        return item

    class Meta:
        db_table = "Clientes"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["id"]


class Bus(models.Model):
    license_plate = models.CharField(max_length=10, verbose_name="Placa")
    chassis_number = models.CharField(max_length=20, verbose_name="Número de chasis")
    engine_number = models.CharField(max_length=20, verbose_name="Número de motor")
    model = models.CharField(max_length=30, verbose_name="Modelo")
    color = models.CharField(max_length=20, verbose_name="Color")
    brand = models.CharField(max_length=30, verbose_name="Marca")
    capacity = models.PositiveIntegerField(verbose_name="Capacidad")
    year = models.PositiveIntegerField(verbose_name="Año")
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return self.license_plate

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = "Buses"
        verbose_name = "Bus"
        verbose_name_plural = "Buses"
        ordering = ["id"]


class Travel(models.Model):
    routeID = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="Ruta")
    busID = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name="Bus")
    departure = models.DateField(default=datetime.now, verbose_name="Fecha de salida")
    departure_time = models.TimeField(
        default=current_time, verbose_name="Hora de salida"
    )
    arrival = models.DateField(default=datetime.now, verbose_name="Fecha de llegada")
    status = models.CharField(
        max_length=10,
        choices=travel_status_choices,
        default="active",
        verbose_name="Estado",
    )

    def __str__(self):
        return f"({self.departure} - {self.departure_time}) {self.busID.license_plate} -> {self.routeID.destination}"

    def toJSON(self):
        item = model_to_dict(self)
        item["route"] = self.routeID.toJSON()
        return item

    class Meta:
        db_table = "Viajes"
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ["id"]


class Parcel(models.Model):
    senderID = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="sent_parcels"
    )
    receiverID = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="received_parcels"
    )
    travelID = models.ForeignKey(Travel, on_delete=models.CASCADE)
    date_joined = models.DateField(
        default=datetime.now, verbose_name="Fecha de registro"
    )
    status = models.CharField(
        max_length=30,
        choices=parcel_choices,
        default="pending",
        verbose_name="Estado",
        blank=True,
    )
    total = models.DecimalField(
        default=0.00,
        max_digits=10,
        decimal_places=2,
        verbose_name="Total Precio de Envío",
    )

    def __str__(self):
        return self.senderID.names

    def toJSON(self):
        data = model_to_dict(self)
        data["senderID"] = (
            f"{self.senderID.names} {self.senderID.surnames}"  # Combina nombres y apellidos
        )
        data["receiverID"] = f"{self.receiverID.names} {self.receiverID.surnames}"
        data["travelID"] = (
            f"{self.travelID.routeID.origin} -> {self.travelID.routeID.destination} ({self.travelID.departure} {self.travelID.departure_time})"
        )
        return data

    class Meta:
        db_table = "Encomiendas"
        verbose_name = "Encomienda"
        verbose_name_plural = "Encomiendas"
        ordering = ["id"]


class ParcelItem(models.Model):
    parcelID = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    weight = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Peso"
    )
    declared_value = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Valor declarado"
    )
    shipping_cost = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Costo de envío"
    )

    def __str__(self):
        return f"Encomienda ID: {self.parcelID.id}, Cantidad: {self.quantity}, Descripción: {self.description or 'Sin descripción'}"

    def toJSON(self):
        data = model_to_dict(self)
        data["parcelID"] = self.parcelID.id  # Solo incluye el ID de la encomienda
        data["description"] = self.description or "Sin descripción"
        return data

    class Meta:
        db_table = "DetallesEncomiendas"
        verbose_name = "Detalle de Encomienda"
        verbose_name_plural = "Deatlle de Encomiendas"
        ordering = ["id"]


class Remittance(models.Model):
    senderID = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="sent_remittances"
    )
    receiverID = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="received_remittances"
    )
    amount_to_send = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Monto a enviar"
    )
    commission_percentage = models.DecimalField(
        default=10,
        max_digits=9,
        decimal_places=2,
        verbose_name="Potcentaje de Comisión",
    )
    commission_amount = models.DecimalField(
        default=0.00,
        max_digits=9,
        decimal_places=2,
        verbose_name="Monto de la Comisión",
    )
    transaction_date = models.DateField(
        default=datetime.now, verbose_name="Fecha de transacción"
    )
    total_amount = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Monto total"
    )
    notes = models.TextField(null=True, blank=True, verbose_name="Observaciones")
    delivery_date = models.DateField(
        null=True, blank=True, default=None, verbose_name="Fecha de entrega"
    )
    status = models.CharField(
        max_length=30,
        choices=remittance_choices,
        default="pending",
        blank=True,
        verbose_name="Estado",
    )

    def __str__(self):
        return f"Giro de {self.senderID.names} a {self.receiverID.names} por {self.amount_to_send}"

    def toJSON(self):
        data = model_to_dict(self)
        data["senderID"] = (
            f"{self.senderID.names} {self.senderID.surnames}"  # Combina nombres y apellidos
        )
        data["receiverID"] = f"{self.receiverID.names} {self.receiverID.surnames}"
        data["transaction_date"] = self.transaction_date.strftime("%Y-%m-%d")
        data["delivery_date"] = (
            self.delivery_date.strftime("%Y-%m-%d") if self.delivery_date else None
        )
        return data

    class Meta:
        db_table = "Giros"
        verbose_name = "Giro"
        verbose_name_plural = "Giros"
        ordering = ["id"]


class Ticket(models.Model):
    clientID = models.ForeignKey(Client, on_delete=models.CASCADE)
    travelID = models.ForeignKey(Travel, on_delete=models.CASCADE)
    purchase_date = models.DateField(
        default=datetime.now, verbose_name="Fecha de compra"
    )
    ticket_type = models.CharField(
        max_length=20,
        choices=ticket_type_choices,
        default="libre",
        verbose_name="Tipo de pasaje",
    )
    total_price = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Precio total"
    )
    status = models.BooleanField(default=True, verbose_name="Estado")

    def __str__(self):
        return f"Ticket de {self.clientID.names} para el viaje {self.travelID.id}"

    def toJSON(self):
        data = model_to_dict(self)
        data["clientID"] = (
            f"{self.clientID.names} {self.clientID.surnames}"  # Combina nombres y apellidos
        )
        data["travelID"] = (
            f"{self.travelID.routeID.origin} -> {self.travelID.routeID.destination} ({self.travelID.departure} {self.travelID.departure_time})"
        )
        return data

    class Meta:
        db_table = "Pasajes"
        verbose_name = "Pasaje"
        verbose_name_plural = "Pasajes"
        ordering = ["id"]


class TicketDetail(models.Model):
    ticketID = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    seat_number = models.IntegerField(default=0, verbose_name="Número de asiento")
    passengerID = models.ForeignKey(
        Client, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Pasajero"
    )
    price = models.DecimalField(
        default=0.00, max_digits=9, decimal_places=2, verbose_name="Precio"
    )

    def __str__(self):
        return f"Pasajero: {self.passengerID.names}, Asiento: {self.seat_number}"

    def toJSON(self):
        data = model_to_dict(self)
        data["ticketID"] = self.ticketID.id
        data["passengerID"] = (
            f"{self.passengerID.names} {self.passengerID.surnames}"  # Combina nombres y apellidos
        )
        return data

    class Meta:
        db_table = "DetallesPasajes"
        verbose_name = "Detalle de Pasaje"
        verbose_name_plural = "Detalle de Pasajes"
        ordering = ["id"]


class DailyCashBox(models.Model):
    date = models.DateField(verbose_name="Fecha", auto_now_add=True)
    total_income = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Total Ingresos"
    )
    total_expenses = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Total Egresos"
    )
    final_balance = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Saldo Final"
    )
    cashbox_type = models.CharField(
        max_length=20, choices=cashbox_type_choices, verbose_name="Tipo de arqueo"
    )
    status = models.CharField(
        max_length=10,
        choices=cashbox_status_choices,
        default="open",
        verbose_name="Estado",
    )

    def __str__(self):
        return f"CashBox {self.id} - {self.date}"

    def toJSON(self):
        data = model_to_dict(self)
        data["cashbox_type"] = {
            "id": self.cashbox_type,
            "name": self.get_cashbox_type_display(),
        }
        data["status"] = {
            "id": self.status,
            "name": self.get_status_display(),
        }
        return data

    class Meta:
        db_table = "CajaDiaria"
        verbose_name = "Caja Diaria"
        verbose_name_plural = "Cajas Diarias"
        ordering = ["id"]


class CashMovement(models.Model):
    cashboxID = models.ForeignKey(
        DailyCashBox, on_delete=models.CASCADE, verbose_name="Caja Diaria"
    )
    movement_type = models.CharField(
        max_length=10, choices=movement_type_choices, verbose_name="Tipo de movimiento"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto")
    payment_method = models.CharField(
        max_length=10, choices=payment_method_choices, verbose_name="Método de pago"
    )
    description = models.TextField(verbose_name="Descripción", null=True, blank=True)
    date = models.DateField(auto_now_add=True, verbose_name="Fecha")
    time = models.TimeField(auto_now_add=True, verbose_name="Hora")
    ticket_id = models.BigIntegerField(
        null=True, blank=True, verbose_name="ID del Ticket"
    )
    parcel_id = models.BigIntegerField(
        null=True, blank=True, verbose_name="ID de la Encomienda"
    )

    def __str__(self):
        return f"Movement {self.movement_id} - CashBox {self.cashbox_id}"

    def toJSON(self):
        data = model_to_dict(self)
        data["cashbox"] = self.cashbox_id
        data["payment_method"] = {
            "id": self.payment_method,
            "name": self.get_payment_method_display(),
        }
        return data

    class Meta:
        db_table = "MovimientosCaja"
        verbose_name = "Movimiento de Caja"
        verbose_name_plural = "Movimientos de Caja"
        ordering = ["id"]
