from django.db import models


class SetupCompany(models.Model):
    company_name = models.CharField(max_length=255, primary_key=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    web = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    vat_no = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.CharField(max_length=50, blank=True, null=True)
    sort_code = models.CharField(max_length=10, blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "setup_company"  # Renamed table


class MItem(models.Model):
    it_id = models.CharField(max_length=10, primary_key=True)  # Primary Key
    desc = models.CharField(max_length=50)  # Description
    date_time = models.DateTimeField(auto_now_add=True)  # Auto-filled date and time
    userid = models.IntegerField()  # User ID

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "M_items"  # Renamed table


class MMetal(models.Model):
    met_id = models.CharField(max_length=10, primary_key=True)  # Primary Key
    desc = models.CharField(max_length=50)  # Description
    date_time = models.DateTimeField(auto_now_add=True)  # Auto-filled date and time
    userid = models.IntegerField()  # User ID

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "M_metals"  # Renamed table


class MMetalProcess(models.Model):
    mepr_id = models.CharField(max_length=10, primary_key=True)  # Primary Key
    desc = models.CharField(max_length=50)  # Description
    date_time = models.DateTimeField(auto_now_add=True)  # Auto-filled date and time
    userid = models.IntegerField()  # User ID

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "M_metalprocess"  # Renamed table


class SerialTable(models.Model):
    sr_code = models.CharField(max_length=10, primary_key=True)  # Primary Key
    count = models.PositiveIntegerField()  # Count (must be positive)
    description = models.CharField(max_length=50)  # Description

    def __str__(self):
        return f"{self.sr_code}: {self.description}"

    class Meta:
        db_table = "serial_table"  # Renamed table


class MTrsItemsMetals(models.Model):
    item = models.ForeignKey(
        MItem, on_delete=models.CASCADE, db_column="it_id"
    )  # Foreign key to MItem
    metal = models.ForeignKey(
        MMetal, on_delete=models.CASCADE, db_column="met_id"
    )  # Foreign key to MMetal

    class Meta:
        db_table = "M_trs_items_metals"  # Renamed table
        unique_together = (
            "item",
            "metal",
        )  # Ensure unique combinations of item and metal

    def __str__(self):
        return f"{self.item.it_id} - {self.metal.met_id}"
