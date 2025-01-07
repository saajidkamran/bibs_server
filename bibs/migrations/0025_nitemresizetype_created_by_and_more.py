# Generated by Django 5.1.3 on 2025-01-07 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0024_rename_nid_nitemresizetype_itmrz_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='nitemresizetype',
            name='created_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='nitemresizetype',
            name='updated_by',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='nitemresizetype',
            name='itmrz_id',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]