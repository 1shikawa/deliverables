# Generated by Django 2.0.7 on 2018-08-14 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0016_auto_20180814_1608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='SmallItems',
            new_name='SmallItem',
        ),
    ]
