# Generated by Django 5.1.3 on 2024-12-01 12:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MItem',
            fields=[
                ('it_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'M_items',
            },
        ),
        migrations.CreateModel(
            name='MMetal',
            fields=[
                ('met_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'M_metals',
            },
        ),
        migrations.CreateModel(
            name='MMetalProcess',
            fields=[
                ('mepr_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'M_metalprocess',
            },
        ),
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
            name='SerialTable',
            fields=[
                ('sr_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('count', models.PositiveIntegerField()),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'serial_table',
            },
        ),
        migrations.CreateModel(
            name='SetupCompany',
            fields=[
                ('company_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('phone_no', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('web', models.URLField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('vat_no', models.CharField(blank=True, max_length=50, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('account_no', models.CharField(blank=True, max_length=50, null=True)),
                ('sort_code', models.CharField(blank=True, max_length=10, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'setup_company',
            },
        ),
        migrations.CreateModel(
            name='MTrsItemsMetals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(db_column='it_id', on_delete=django.db.models.deletion.CASCADE, to='bibs.mitem')),
                ('metal', models.ForeignKey(db_column='met_id', on_delete=django.db.models.deletion.CASCADE, to='bibs.mmetal')),
            ],
            options={
                'db_table': 'M_trs_items_metals',
                'unique_together': {('item', 'metal')},
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
