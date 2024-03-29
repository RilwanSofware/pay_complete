# Generated by Django 4.1.7 on 2023-03-21 17:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0005_alter_transferreceipient_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferreceipient',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transferreceipient',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 21, 17, 28, 58, 259879, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
