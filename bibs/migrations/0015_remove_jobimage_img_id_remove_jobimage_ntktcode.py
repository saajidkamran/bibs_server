# Generated by Django 5.1.3 on 2025-04-06 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0014_rename_createdby_cashcustomer_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobimage',
            name='img_id',
        ),
        migrations.RemoveField(
            model_name='jobimage',
            name='nTKTCODE',
        ),
    ]
