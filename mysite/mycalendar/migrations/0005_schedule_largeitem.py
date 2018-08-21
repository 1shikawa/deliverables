# Generated by Django 2.0.7 on 2018-08-02 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycalendar', '0004_schedule_register'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='LargeItem',
            field=models.CharField(choices=[('HMK・旧シス対応', 'HMK・旧シス対応'), ('サービス対応', 'サービス対応'), ('抽出', '抽出'), ('PJT/案件', 'PJT/案件')], default='HMK・旧シス対応', max_length=50, verbose_name='大項目'),
        ),
    ]
