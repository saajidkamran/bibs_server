# Generated by Django 5.1.3 on 2024-11-24 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MItem',
            fields=[
                ('it_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=50)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('userid', models.IntegerField()),
            ],
        ),
    ]