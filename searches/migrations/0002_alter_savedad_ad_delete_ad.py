# Generated by Django 5.1.4 on 2025-01-28 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_roomlisting_postcode'),
        ('searches', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedad',
            name='ad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.roomlisting'),
        ),
        migrations.DeleteModel(
            name='Ad',
        ),
    ]
