# Generated by Django 4.2.2 on 2023-07-06 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_product_color_remove_productattribute_color_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductAttribute',
        ),
    ]
