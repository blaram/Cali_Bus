# Generated by Django 5.1.2 on 2024-11-16 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ci',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Cédula de Identidad'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d', verbose_name='Imagen'),
        ),
    ]
