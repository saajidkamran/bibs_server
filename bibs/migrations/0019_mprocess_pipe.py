# Generated by Django 5.1.3 on 2025-01-07 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0018_nprocesspipetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='mprocess',
            name='pipe',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]