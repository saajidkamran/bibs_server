# Generated by Django 5.1.3 on 2025-01-13 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0027_naccountsummary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='naccountsummary',
            name='nTotOutStand',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=20),
        ),
        migrations.AlterModelTable(
            name='naccountsummary',
            table='naccount_summary',
        ),
    ]
