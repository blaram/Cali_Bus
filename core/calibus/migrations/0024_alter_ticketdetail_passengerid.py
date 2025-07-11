# Generated by Django 5.1.2 on 2025-06-21 21:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calibus", "0023_remove_ticket_purchase_time_alter_ticket_ticket_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticketdetail",
            name="passengerID",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="calibus.client",
                verbose_name="Pasajero",
            ),
        ),
    ]
