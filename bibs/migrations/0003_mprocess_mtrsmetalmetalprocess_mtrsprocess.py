# Generated by Django 5.1.3 on 2024-11-30 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0002_rename_date_time_mitem_created_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MProcess',
            fields=[
                ('pr_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'M_process',
            },
        ),
        migrations.CreateModel(
            name='MTrsMetalMetalProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metal', models.ForeignKey(db_column='met_id', on_delete=django.db.models.deletion.CASCADE, to='bibs.mmetal')),
                ('metal_process', models.ForeignKey(db_column='mepr_id', on_delete=django.db.models.deletion.CASCADE, to='bibs.mmetalprocess')),
            ],
            options={
                'db_table': 'M_trs_metals_metalprocess',
                'unique_together': {('metal_process', 'metal')},
            },
        ),
        migrations.CreateModel(
            name='MTrsProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metal_process', models.ForeignKey(db_column='mepr_id', on_delete=django.db.models.deletion.CASCADE, to='bibs.mmetalprocess')),
                ('process', models.ForeignKey(db_column='pr_id', on_delete=django.db.models.deletion.CASCADE, to='bibs.mprocess')),
            ],
            options={
                'db_table': 'M_trs_process',
                'unique_together': {('metal_process', 'process')},
            },
        ),
    ]
