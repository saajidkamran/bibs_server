# Generated by Django 5.1.3 on 2025-01-10 01:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0025_nitemresizetype_created_by_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MTrsProcessType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq_no', models.IntegerField(default=0)),
                ('process', models.ForeignKey(db_column='pr_id', on_delete=django.db.models.deletion.CASCADE, to='bibs.mprocess')),
                ('process_type', models.ForeignKey(db_column='pt_id', on_delete=django.db.models.deletion.CASCADE, to='bibs.nprocesstype')),
            ],
            options={
                'db_table': 'M_trs_process_type',
                'unique_together': {('process_type', 'process')},
            },
        ),
    ]