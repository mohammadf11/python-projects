# Generated by Django 3.2 on 2022-08-24 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='vote',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]