# Generated by Django 5.1.3 on 2025-01-27 06:35
from django.db import migrations, models


def update_ntdue(apps, schema_editor):
    Ticket = apps.get_model("bibs", "Ticket")
    db_alias = schema_editor.connection.alias
    Ticket.objects.using(db_alias).update(nTDue=models.F("nTCost") - models.F("nTPaid"))


class Migration(migrations.Migration):

    dependencies = [
        (
            "bibs",
            "0006_alter_ticket_iscashcustomer",
        ),  # Replace with the correct dependency
    ]

    operations = [
        migrations.RunPython(update_ntdue),
    ]
