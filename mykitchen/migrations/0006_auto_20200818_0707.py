# Generated by Django 2.2.14 on 2020-08-18 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mykitchen', '0005_auto_20200818_0654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storagelocation',
            old_name='editted_by',
            new_name='edited_by',
        ),
    ]