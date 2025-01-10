# Generated by Django 5.1.3 on 2025-01-07 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bibs', '0019_mprocess_pipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='NItemResizeType',
            fields=[
                ('nId', models.AutoField(primary_key=True, serialize=False)),
                ('nType', models.CharField(max_length=50)),
                ('nSeqNo', models.IntegerField()),
                ('nActive', models.BooleanField(default=False)),
                ('nCreatedDate', models.DateTimeField(auto_now_add=True)),
                ('nUpdatedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NProcessType',
            fields=[
                ('pt_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('processNa', models.CharField(max_length=50)),
                ('processPipe', models.IntegerField()),
                ('nActive', models.BooleanField(default=False)),
                ('nCreatedDate', models.DateTimeField(auto_now_add=True)),
                ('nUpdatedDate', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
