# Generated by Django 5.1.2 on 2024-11-05 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calibus', '0004_remove_product_cat_remove_detsale_prod_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='origin',
            field=models.CharField(max_length=100, verbose_name='Origen'),
        ),
    ]