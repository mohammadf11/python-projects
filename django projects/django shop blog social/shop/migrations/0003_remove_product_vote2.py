# Generated by Django 3.2 on 2022-08-25 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_vote2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='vote2',
        ),
    ]
