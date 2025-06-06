# Generated by Django 5.1.2 on 2025-03-13 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calibus", "0009_alter_client_nationality"),
    ]

    operations = [
        migrations.RenameField(
            model_name="travel",
            old_name="rou",
            new_name="routeID",
        ),
        migrations.AddField(
            model_name="travel",
            name="busID",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="calibus.bus",
                verbose_name="Bus",
            ),
            preserve_default=False,
        ),
    ]
