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
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = "setup_company"


class MItem(models.Model):
    it_id = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "M_items"


class MMetal(models.Model):
    met_id = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "M_metals"


class MMetalProcess(models.Model):
    mepr_id = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "M_metalprocess"


class MProcess(models.Model):
    pr_id = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "M_process"


class SerialTable(models.Model):
    sr_code = models.CharField(max_length=10, primary_key=True)  # Primary Key
    count = models.PositiveIntegerField()  # Count (must be positive)
    description = models.CharField(max_length=50)  # Description

    def __str__(self):
        return self.description

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
        db_table = "M_trsitemsmetals"  # Renamed table
        unique_together = (
            "item",
            "metal",
        )  # Ensure unique combinations of item and metal

    def __str__(self):
        return f"{self.item.it_id} - {self.metal.met_id}"


class MTrsMetalMetalProcess(models.Model):
    metal = models.ForeignKey(
        MMetal, on_delete=models.CASCADE, db_column="met_id"
    )  # Foreign key to MItem
    metal_process = models.ForeignKey(
        MMetalProcess, on_delete=models.CASCADE, db_column="mepr_id"
    )  # Foreign key to MMetal

    class Meta:
        db_table = "M_trs_metals_metalprocess"  # Renamed table
        unique_together = (
            "metal_process",
            "metal",
        )  # Ensure unique combinations of item and metal

    def __str__(self):
        return f"{self.metal_process.mepr_id} - {self.metal.met_id}"


class MTrsProcess(models.Model):
    process = models.ForeignKey(
        MProcess, on_delete=models.CASCADE, db_column="pr_id"
    )  # Foreign key to MItem
    metal_process = models.ForeignKey(
        MMetalProcess, on_delete=models.CASCADE, db_column="mepr_id"
    )  # Foreign key to MMetal

    class Meta:
        db_table = "M_trs_process"  # Renamed table
        unique_together = (
            "metal_process",
            "process",
        )  # Ensure unique combinations of item and metal

    def __str__(self):
        return f"{self.process.pr_id} - {self.metal_process.mepr_id}"
