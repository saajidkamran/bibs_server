# Generated by Django 5.1.3 on 2025-01-22 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0002_alter_setupcompany_vat_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setupcompany',
            name='vat_no',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
