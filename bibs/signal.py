from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    MItem,
    MMetal,
    MMetalProcess,
    Employee,
    Customer,
    SerialTable,
)


def update_serial_table_entry(sr_code, model):
    count = model.objects.count()
    SerialTable.objects.update_or_create(
        sr_code=sr_code,
        defaults={
            "count": count,
        },
    )


@receiver(post_save, sender=MItem)
@receiver(post_delete, sender=MItem)
def update_item_count(sender, instance, **kwargs):
    update_serial_table_entry("itm", MItem)


@receiver(post_save, sender=MMetal)
@receiver(post_delete, sender=MMetal)
def update_metal_count(sender, instance, **kwargs):
    update_serial_table_entry("met", MMetal)


@receiver(post_save, sender=MMetalProcess)
@receiver(post_delete, sender=MMetalProcess)
def update_metal_process_count(sender, instance, **kwargs):
    update_serial_table_entry("mepr", MMetalProcess)


@receiver(post_save, sender=Employee)
@receiver(post_delete, sender=Employee)
def update_employee_count(sender, instance, **kwargs):
    update_serial_table_entry("emp", Employee)


@receiver(post_save, sender=Customer)
@receiver(post_delete, sender=Customer)
def update_customer_count(sender, instance, **kwargs):
    update_serial_table_entry("cus", Customer)
