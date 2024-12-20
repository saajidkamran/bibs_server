from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    MItem,
    MMetal,
    MMetalProcess,
    Employee,
    Customer,
    SerialTable,
    Job,
    Ticket,
    MProcess,
)


def increment_serial_table_entry(sr_code):
    try:
        entry = SerialTable.objects.get(sr_code=sr_code)
        # entry.count += 1
        entry.save()
    except SerialTable.DoesNotExist:
        SerialTable.objects.create(sr_code=sr_code, count=1)


@receiver(post_save, sender=Ticket)
def increment_item_count(sender, instance, created, **kwargs):
    if created:  # Only increment when a new job is created
        increment_serial_table_entry("tkt")


@receiver(post_save, sender=Job)
def increment_item_count(sender, instance, created, **kwargs):
    if created:  # Only increment when a new job is created
        increment_serial_table_entry("job")


@receiver(post_save, sender=MItem)
def increment_item_count(sender, instance, created, **kwargs):
    if created:  # Only increment when a new item is created
        increment_serial_table_entry("itm")


@receiver(post_save, sender=MMetal)
def increment_metal_count(sender, instance, created, **kwargs):
    if created:
        increment_serial_table_entry("met")


@receiver(post_save, sender=MMetalProcess)
def increment_metal_process_count(sender, instance, created, **kwargs):
    if created:
        increment_serial_table_entry("mepr")


@receiver(post_save, sender=Employee)
def increment_employee_count(sender, instance, created, **kwargs):
    if created:
        increment_serial_table_entry("emp")


@receiver(post_save, sender=Customer)
def increment_customer_count(sender, instance, created, **kwargs):
    if created:
        increment_serial_table_entry("cus")


@receiver(post_save, sender=MProcess)
def increment_customer_count(sender, instance, created, **kwargs):
    if created:
        increment_serial_table_entry("prc")
