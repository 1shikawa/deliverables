# Generated by Django 2.0.7 on 2018-08-20 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0021_auto_20180816_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='LargeItem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mycalendar.LargeItem'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='MiddleItem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mycalendar.MiddleItem'),
        ),
    ]
