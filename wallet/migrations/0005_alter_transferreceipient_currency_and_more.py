# Generated by Django 4.1.7 on 2023-03-21 17:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_transferreceipient_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferreceipient',
            name='currency',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='transferreceipient',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 21, 17, 27, 16, 649618, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]