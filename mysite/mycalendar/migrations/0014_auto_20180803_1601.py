# Generated by Django 2.0.7 on 2018-08-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0013_auto_20180803_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='kosu',
            field=models.IntegerField(blank=True, default=0, verbose_name='時間（分）'),
        ),
    ]
