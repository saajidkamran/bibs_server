# Generated by Django 5.1.3 on 2024-12-20 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0014_menuaccessvisibility'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('menu_id', models.AutoField(primary_key=True, serialize=False)),
                ('menu_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'menu',
            },
        ),
    ]
