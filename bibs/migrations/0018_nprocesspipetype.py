# Generated by Django 5.1.3 on 2025-01-07 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0017_alter_mitem_table_alter_mmetal_table_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NProcessPipeType',
            fields=[
                ('nPTId', models.AutoField(primary_key=True, serialize=False)),
                ('nProType', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
