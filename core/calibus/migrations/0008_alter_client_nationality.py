# Generated by Django 5.1.2 on 2025-03-11 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calibus", "0007_bus_client_date_of_birth_client_nationality"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="nationality",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="Nacionalidad"
            ),
        ),
    ]
