from django.db import models
import uuid  # For UUIDField


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
    seq_no = models.CharField(max_length=10)
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
        db_table = "M_trs_items_metals"  # Renamed table
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


class Employee(models.Model):
    nId = models.AutoField(primary_key=True)  # Primary Key
    nEMPCODE = models.CharField(max_length=50, unique=True)  # Employee Code
    nUserRole = models.IntegerField(null=True, blank=True)  # User Role
    nActive = models.BooleanField(default=False)  # Active status
    nFirstName = models.CharField(max_length=100, null=True, blank=True)  # First Name
    nSurName = models.CharField(max_length=100, null=True, blank=True)  # Surname
    nAddress1 = models.CharField(
        max_length=255, null=True, blank=True
    )  # Address line 1
    nAddress2 = models.CharField(
        max_length=255, null=True, blank=True
    )  # Address line 2
    nAddress3 = models.CharField(
        max_length=255, null=True, blank=True
    )  # Address line 3
    nTown = models.CharField(max_length=100, null=True, blank=True)  # Town
    nPostCode = models.CharField(max_length=20, null=True, blank=True)  # Postcode
    nPhone = models.CharField(max_length=20, null=True, blank=True)  # Phone
    nMobile = models.CharField(max_length=20, null=True, blank=True)  # Mobile
    nEmail = models.EmailField(max_length=100, null=True, blank=True)  # Email
    nBasicSal = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.0
    )  # Basic Salary
    nOverTime = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.0
    )  # Overtime
    nNoOfAppLeave = models.IntegerField(default=0)  # Number of Approved Leaves
    nLeaveTaken = models.IntegerField(default=0)  # Number of Leaves Taken
    nCreatedDate = models.DateTimeField(auto_now_add=True)  # Creation Date
    nUpdatedDate = models.DateTimeField(auto_now=True)  # Update Date
    nCreatedBy = models.CharField(max_length=50, null=True, blank=True)  # Created By
    nUpdatedBy = models.CharField(max_length=50, null=True, blank=True)  # Updated By
    nFSID = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )  # Foreign System ID (GUID)
    nImage = models.TextField(null=True, blank=True)  # Image
    nPwdHash = models.CharField(max_length=256, null=True, blank=True)  # Password Hash
    nPwdSalt = models.CharField(max_length=256, null=True, blank=True)  # Password Salt

    def __str__(self):
        return self.nEMPCODE


class Customer(models.Model):
    nId = models.AutoField(primary_key=True)  # Primary Key
    nCUSCODE = models.CharField(max_length=50, unique=True)  # Customer Code
    nCTId = models.IntegerField(null=True, blank=True)  # Customer Type ID
    nActive = models.BooleanField(default=False)  # Active Status
    nComName = models.CharField(max_length=255, null=True, blank=True)  # Company Name
    nSurName = models.CharField(max_length=255, null=True, blank=True)  # Surname
    nFirstName = models.CharField(max_length=255, null=True, blank=True)  # First Name
    nAddress1 = models.CharField(
        max_length=255, null=True, blank=True
    )  # Address Line 1
    nAddress2 = models.CharField(
        max_length=255, null=True, blank=True
    )  # Address Line 2
    nAddress3 = models.CharField(
        max_length=255, null=True, blank=True
    )  # Address Line 3
    nCity = models.CharField(max_length=100, null=True, blank=True)  # City
    nState = models.CharField(max_length=100, null=True, blank=True)  # State
    nPostCode = models.CharField(max_length=20, null=True, blank=True)  # Postcode
    nPhone1 = models.CharField(max_length=20, null=True, blank=True)  # Phone 1
    nPhone2 = models.CharField(max_length=20, null=True, blank=True)  # Phone 2
    nMobile = models.CharField(max_length=20, null=True, blank=True)  # Mobile
    nFax = models.CharField(max_length=20, null=True, blank=True)  # Fax
    nEmail = models.EmailField(max_length=255, null=True, blank=True)  # Email
    nWebsite = models.URLField(max_length=255, null=True, blank=True)  # Website
    nCreditLimit = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.0
    )  # Credit Limit
    nVAT = models.BooleanField(default=False)  # VAT Registration Status
    nCreatedDate = models.DateTimeField(auto_now_add=True)  # Creation Date
    nUpdatedDate = models.DateTimeField(auto_now=True)  # Update Date
    nCreatedBy = models.CharField(max_length=50, null=True, blank=True)  # Created By
    nUpdatedBy = models.CharField(max_length=50, null=True, blank=True)  # Updated By
    nSMS = models.BooleanField(default=False)  # SMS Notifications

    def __str__(self):
        return f"{self.nCUSCODE} - {self.nComName}"


class Ticket(models.Model):
    nId = models.AutoField(primary_key=True)  # Primary Key
    nTKTCODE = models.CharField(max_length=20, unique=True)  # Ticket Code
    nStatID = models.IntegerField()  # Status ID
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="tickets"
    )  # Foreign Key to Customer (one-to-many)
    nDocNo = models.CharField(max_length=50, null=True, blank=True)  # Document Number
    nDueDate = models.DateField()  # Due Date
    nDueTime = models.TimeField()  # Due Time
    nTItems = models.IntegerField(default=0)  # Total Items
    nCalVat = models.DecimalField(max_digits=10, decimal_places=2)  # VAT Calculation
    nCostNoVAT = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Cost Without VAT
    nTCost = models.DecimalField(max_digits=10, decimal_places=2)  # Total Cost
    nTPaid = models.DecimalField(max_digits=10, decimal_places=2)  # Total Paid
    nTDue = models.DecimalField(max_digits=10, decimal_places=2)  # Total Due
    multipleImages = models.BooleanField(default=False)  # Multiple Images
    isCashCustomer = models.BooleanField(default=False)  # Cash Customer
    isCusNotSigned = models.BooleanField(default=False)  # Customer Not Signed
    nFSID = models.UUIDField(default=None, null=True, blank=True)  # FSID (GUID)
    nCusSignImage = models.TextField(null=True, blank=True)  # Customer Signed Image
    nComments = models.TextField(null=True, blank=True)  # Comments
    nActive = models.BooleanField(default=True)  # Active Status
    nInvoice = models.BooleanField(default=False)  # Invoice Status
    nAcceptedDate = models.DateTimeField(auto_now_add=True)  # Accepted Date
    nReadyDate = models.DateTimeField(null=True, blank=True)  # Ready Date
    nReleasedDate = models.DateTimeField(null=True, blank=True)  # Released Date
    nAcceptedBy = models.CharField(max_length=50, null=True, blank=True)  # Accepted By
    nReadyBy = models.CharField(max_length=50, null=True, blank=True)  # Ready By
    nReleasedBy = models.CharField(max_length=50, null=True, blank=True)  # Released By

    def __str__(self):
        return self.nTKTCODE

    class Meta:
        db_table = "tb_tickets"  # Set table name


class Job(models.Model):
    nId = models.AutoField(primary_key=True)  # Primary Key
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="jobs"
    )  # Foreign Key to Ticket (one-to-many relationship)
    nJOBCODE = models.CharField(max_length=50, unique=True)  # Job Code
    nJStatID = models.IntegerField()  # Job Status ID
    nIQty = models.IntegerField(default=1)  # Item Quantity
    nPrice = models.DecimalField(max_digits=10, decimal_places=2)  # Price
    nFSID = models.UUIDField(default=None, null=True, blank=True)  # FSID (GUID)
    nImage = models.TextField(null=True, blank=True)  # Image data
    nItem = models.CharField(max_length=255, null=True, blank=True)  # Item Description
    nMetal = models.CharField(
        max_length=255, null=True, blank=True
    )  # Metal Description
    nJobDesc = models.TextField(null=True, blank=True)  # Job Description
    nJobDescHTML = models.TextField(null=True, blank=True)  # Job Description (HTML)
    nActive = models.BooleanField(default=True)  # Active Status

    def __str__(self):
        return self.nJOBCODE

    class Meta:
        db_table = "tb_jobs"  # Set table name


class JobImage(models.Model):
    nId = models.AutoField(primary_key=True)  # Primary Key
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="images"
    )  # Foreign Key to Job (one-to-many relationship)
    nTKTCODE = models.CharField(max_length=50)  # Ticket Code
    nJOBCODE = models.CharField(max_length=50)  # Job Code
    img_id = models.CharField(max_length=100, unique=True)  # Image ID
    img_location = models.TextField()  # Image Location or Base64 Data

    def __str__(self):
        return self.img_id

    class Meta:
        db_table = "tb_jobs_images"  # Set table name
