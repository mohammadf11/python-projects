# Generated by Django 3.2 on 2022-08-24 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vote2',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
