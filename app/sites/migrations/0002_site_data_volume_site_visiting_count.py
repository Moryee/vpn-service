# Generated by Django 4.1.1 on 2024-01-25 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='data_volume',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='site',
            name='visiting_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
