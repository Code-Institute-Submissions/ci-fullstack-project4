# Generated by Django 2.2.14 on 2020-08-27 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mykitchen', '0002_auto_20200823_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storagelocation',
            name='storage_temperature',
            field=models.IntegerField(blank=True, help_text='deg Celsius', null=True),
        ),
    ]
