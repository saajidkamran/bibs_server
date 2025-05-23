from django.db import models
import uuid  # For UUIDField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class SetupCompany(models.Model):
    company_name = models.CharField(max_length=255, primary_key=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    web = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    vat_no = models.DecimalField(max_digits=5, decimal_places=2)
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
    nActive = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "nitems"


class MMetal(models.Model):
    met_id = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=50)
    nActive = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "nmetals"


class MMetalProcess(models.Model):
    mepr_id = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=50)
    nActive = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "nmetalprocess"


class MProcess(models.Model):
    pr_id = models.CharField(max_length=10, primary_key=True)
    desc = models.CharField(max_length=50)
    pipe = models.CharField(max_length=50)
    nActive = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.desc

    class Meta:
        db_table = "nprocess"


class NProcessType(models.Model):
    pt_id = models.CharField(max_length=10, primary_key=True)
    processName = models.CharField(
        max_length=50
    )  # Assuming `processNa` is a string field
    processPipe = models.CharField(
        max_length=50
    )  # Assuming `processNa` is a string field
    nActive = models.BooleanField(default=False)  # Active status
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    nCreatedDate = models.DateTimeField(auto_now_add=True)  # Auto-generated on creation
    nUpdatedDate = models.DateTimeField(auto_now=True)  # Auto-updated on modification

    def __str__(self):
        return f"{self.processNa} ({self.pt_id})"

    class Meta:
        db_table = "nprocesstype"  # Specify table name


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
    seq_no = models.IntegerField(default=0)  # Sequence Number

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
    )  # Foreign key to MMetalProcess
    seq_no = models.IntegerField(default=0)  # Sequence Number

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
    )  # Foreign key to MMetalProcess
    seq_no = models.IntegerField(default=0)  # Sequence Number

    class Meta:
        db_table = "M_trs_process"  # Renamed table
        unique_together = (
            "metal_process",
            "process",
        )  # Ensure unique combinations of metal_process and process

    def __str__(self):
        return f"{self.process.pr_id} - {self.metal_process.mepr_id}"


class MTrsProcessType(models.Model):
    process_type = models.ForeignKey(
        NProcessType, on_delete=models.CASCADE, db_column="pt_id"
    )
    process = models.ForeignKey(MProcess, on_delete=models.CASCADE, db_column="pr_id")

    seq_no = models.IntegerField(default=0)  # Sequence Number

    class Meta:
        db_table = "M_trs_process_type"
        unique_together = (
            "process_type",
            "process",
        )

    def __str__(self):
        return f"{self.process.pr_id} - {self.process_type.pt_id}"




class Employee(AbstractBaseUser, PermissionsMixin):
    nId = models.AutoField(primary_key=True)
    nEMPCODE = models.CharField(max_length=50, unique=True)
    nUserRole = models.IntegerField(null=True, blank=True)
    nActive = models.BooleanField(default=False)
    nFirstName = models.CharField(max_length=100, null=True, blank=True)
    nSurName = models.CharField(max_length=100, null=True, blank=True)
    nAddress1 = models.CharField(max_length=255, null=True, blank=True)
    nAddress2 = models.CharField(max_length=255, null=True, blank=True)
    nAddress3 = models.CharField(max_length=255, null=True, blank=True)
    nTown = models.CharField(max_length=100, null=True, blank=True)
    nPostCode = models.CharField(max_length=20, null=True, blank=True)
    nPhone = models.CharField(max_length=20, null=True, blank=True)
    nMobile = models.CharField(max_length=20, null=True, blank=True)
    nEmail = models.EmailField(max_length=100, unique=True)  # <-- make sure `unique`
    nBasicSal = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    nOverTime = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    nNoOfAppLeave = models.IntegerField(default=0)
    nLeaveTaken = models.IntegerField(default=0)
    nCreatedDate = models.DateTimeField(auto_now_add=True)
    nUpdatedDate = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    nFSID = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nImage = models.TextField(null=True, blank=True)
    is_first_login = models.BooleanField(default=True)
    password = models.CharField(max_length=128)  

    # Django AUTH fields
    USERNAME_FIELD = "nEmail"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nEMPCODE


class Customer(models.Model):
    nCUSCODE = models.CharField(max_length=50, primary_key=True)  # Primary Key
    nCTId = models.IntegerField(null=True, blank=True)
    nActive = models.BooleanField(default=False)
    nComName = models.CharField(max_length=255, null=True, blank=True)
    nSurName = models.CharField(max_length=255, null=True, blank=True)
    nFirstName = models.CharField(max_length=255, null=True, blank=True)
    nAddress1 = models.CharField(max_length=255, null=True, blank=True)
    nAddress2 = models.CharField(max_length=255, null=True, blank=True)
    nAddress3 = models.CharField(max_length=255, null=True, blank=True)
    nCity = models.CharField(max_length=100, null=True, blank=True)
    nState = models.CharField(max_length=100, null=True, blank=True)
    nPostCode = models.CharField(max_length=20, null=True, blank=True)
    nPhone1 = models.CharField(max_length=20, null=True, blank=True)
    nPhone2 = models.CharField(max_length=20, null=True, blank=True)
    nMobile = models.CharField(max_length=20, null=True, blank=True)
    nFax = models.CharField(max_length=20, null=True, blank=True)
    nEmail = models.EmailField(max_length=255, null=True, blank=True)
    nWebsite = models.URLField(max_length=255, null=True, blank=True)
    nCreditLimit = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    nVAT = models.BooleanField(default=False)
    nCreatedDate = models.DateTimeField(auto_now_add=True)
    nUpdatedDate = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    nSMS = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nCUSCODE} - {self.nComName}"

    class Meta:
        db_table = "bibs_customer"


class Ticket(models.Model):
    nTKTCODE = models.CharField(max_length=20, primary_key=True, unique=True)
    nStatID = models.IntegerField(default=1)  # Status ID
    customer = models.ForeignKey(
        Customer,
        to_field="nCUSCODE",
        db_column="nCUSCODE",
        on_delete=models.SET_NULL,  # Use SET_NULL to keep tickets even if the customer is deleted
        related_name="tickets",
        null=True,  # Allow NULL values
        blank=True,  # Allow blank values in forms
    )
    nDocNo = models.CharField(max_length=50, null=True, blank=True)
    nDueDate = models.DateField()
    nDueTime = models.TimeField()
    nTItems = models.IntegerField(default=0)
    nCalVat = models.DecimalField(max_digits=10, decimal_places=2)
    nCostNoVAT = models.DecimalField(max_digits=10, decimal_places=2)
    nTCost = models.DecimalField(max_digits=10, decimal_places=2)
    nTPaid = models.DecimalField(max_digits=10, decimal_places=2)
    nTDue = models.DecimalField(max_digits=10, decimal_places=2)
    multipleImages = models.BooleanField(default=False)
    isCashCustomer = models.IntegerField(default=0)
    isCusNotSigned = models.IntegerField(default=0)
    nFSID = models.IntegerField(default=1)
    nCusSignImage = models.TextField(null=True, blank=True)
    nComments = models.TextField(null=True, blank=True)
    nActive = models.BooleanField(default=True)
    nInvoice = models.BooleanField(default=False)
    nAcceptedDate = models.DateTimeField(auto_now_add=True)
    nReadyDate = models.DateTimeField(null=True, blank=True)
    nReleasedDate = models.DateTimeField(null=True, blank=True)
    nAcceptedBy = models.CharField(max_length=50, null=True, blank=True)
    nReadyBy = models.CharField(max_length=50, null=True, blank=True)
    nReleasedBy = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Automatically update nTDue before saving the object.
        """
        # Calculate nTDue
        self.nTDue = self.nTCost - self.nTPaid
        # Call the default save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nTKTCODE

    class Meta:
        db_table = "tb_tickets"


class Job(models.Model):
    nId = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(
        Ticket,
        to_field="nTKTCODE",
        db_column="nTKTCODE",
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    nJOBCODE = models.CharField(max_length=50, unique=True)
    nJStatID = models.IntegerField()
    nIQty = models.IntegerField(default=1)
    nPrice = models.DecimalField(max_digits=10, decimal_places=2)
    nFSID = models.UUIDField(default=None, null=True, blank=True)
    nImage = models.TextField(null=True, blank=True)
    nItem = models.CharField(max_length=255, null=True, blank=True)
    nMetal = models.CharField(max_length=255, null=True, blank=True)
    nJobDesc = models.TextField(null=True, blank=True)
    nJobDescHTML = models.TextField(null=True, blank=True)
    nActive = models.BooleanField(default=True)

    def __str__(self):
        return self.nJOBCODE

    class Meta:
        db_table = "tb_jobs"


class JobImage(models.Model):
    nId = models.AutoField(primary_key=True)  # Primary Key
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="images"
    )  # Foreign Key to Job (one-to-many relationship)
    nJOBCODE = models.CharField(max_length=50)  # Job Code
    img_location = models.TextField()  # Image Location or Base64 Data

    def __str__(self):
        return self.nId

    class Meta:
        db_table = "tb_jobs_images"  # Set table name


class UserGroup(models.Model):
    user_group_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    group_name = models.CharField(max_length=50, unique=True)  # Unique group name

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = "user_groups"  # Specify table name


class MenuAccessVisibility(models.Model):
    menu_id = models.AutoField(primary_key=True)  # Primary key for this table
    menu_name = models.CharField(max_length=50)  # Name of the menu
    user_group = models.ForeignKey(
        "UserGroup",
        on_delete=models.CASCADE,
        db_column="user_group_id",
        related_name="menu_access",
    )  # Foreign key linking to UserGroup
    visible_no = models.CharField(
        max_length=10, null=True, blank=True
    )  # Visibility flag

    def __str__(self):
        return f"{self.menu_name} ({self.visible_no})"

    class Meta:
        db_table = "menu_access_visibility"  # Specify table name


class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)  # Primary Key for Menu table
    menu_name = models.CharField(max_length=100, unique=True)  # Menu name

    def __str__(self):
        return self.menu_name

    class Meta:
        db_table = "menu"  # Specify table name


class AccessRights(models.Model):
    access_right_id = models.AutoField(
        primary_key=True
    )  # Primary key for the AccessRights table
    user_group = models.ForeignKey(
        "UserGroup",
        on_delete=models.CASCADE,
        db_column="user_group_id",
        related_name="access_rights",
    )  # Foreign key referencing UserGroup
    menu = models.ForeignKey(
        "Menu",
        on_delete=models.CASCADE,
        db_column="menu_id",
        related_name="access_rights",
    )  # Foreign key referencing Menu
    add = models.BooleanField(default=False)  # Permission to add
    edit = models.BooleanField(default=False)  # Permission to edit
    delete = models.BooleanField(default=False)  # Permission to delete
    update = models.BooleanField(default=False)  # Permission to update

    def __str__(self):
        return f"UserGroup: {self.user_group.group_name}, Menu: {self.menu.menu_name}"

    class Meta:
        db_table = "access_rights"  # Specify table name
        unique_together = ("user_group", "menu")  # Ensure unique combinat


class NProcessPipeType(models.Model):
    nPTId = models.AutoField(primary_key=True)
    nProType = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nProType


class NItemResizeType(models.Model):
    itmrz_id = models.CharField(max_length=10, primary_key=True)
    nType = models.CharField(max_length=50)  # Assuming `nType` is a string field
    nSeqNo = models.IntegerField()  # Sequence Number
    nActive = models.BooleanField(default=False)  # Active Status
    nCreatedDate = models.DateTimeField(auto_now_add=True)  # Auto-generated on creation
    nUpdatedDate = models.DateTimeField(auto_now=True)  # Auto-updated on modification
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nType} ({self.itmrz_id})"

    class Meta:
        db_table = "nitemresizetype"  # Specify table name


class NAccountSummary(models.Model):
    nID = models.BigAutoField(primary_key=True)
    nACUSID = models.CharField(max_length=50, null=False)  # Customer ID
    nTickets = models.DecimalField(max_digits=20, decimal_places=10)
    nPayment = models.DecimalField(max_digits=20, decimal_places=2)
    nTotOutStand = models.DecimalField(max_digits=20, decimal_places=4, default=0.0)
    # nLastUDate = models.DateField(null=True, blank=True)  # Handles NULL dates
    nCreatedDate = models.DateTimeField(auto_now_add=True)  # Auto-generated on creation
    created_by = models.CharField(max_length=50, blank=True, null=True)
    nUpdatedDate = models.DateTimeField(auto_now=True)  # Auto-updated on modification
    updated_by = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Account Summary ID: {self.nID}"

    def update_outstanding(self):
        """
        Update nTotOutStand as nTickets - nPayment.
        """
        self.nTotOutStand = self.nTickets - self.nPayment
        self.save()

    class Meta:
        db_table = "nAccountSummary"


class NPaymentType(models.Model):
    nId = models.AutoField(primary_key=True)
    nType = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nType  # String representation of the model

    class Meta:
        db_table = "nPaymentType"  # Custom table name


class NPayment(models.Model):
    nId = models.AutoField(primary_key=True)
    nCusID = models.CharField(max_length=50)  # Customer ID
    nMonWeek = models.IntegerField()  # Month/Week
    nPaidAmount = models.DecimalField(max_digits=10, decimal_places=2)  # Paid Amount
    nPayType = models.IntegerField()  # Payment Type (reference to NPaymentType)
    paymentDetail = models.CharField(
        max_length=255, null=True, blank=True
    )  # Payment Details
    nComments = models.TextField(null=True, blank=True)  # Comments
    nCreatedDate = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    nCreatedBy = models.CharField(max_length=50, null=True, blank=True)  # Created By

    def __str__(self):
        return f"{self.nCusID} - {self.nPaidAmount}"

    class Meta:
        db_table = "nPayment"


class CashCustomer(models.Model):
    cashCusID = models.CharField(max_length=50, primary_key=True)  # Primary Key
    Name = models.CharField(max_length=255)  # Customer Nam
    Address = models.TextField(null=True, blank=True)  # Customer Address
    CreatedDate = models.DateTimeField(auto_now_add=True)  # Auto set on creation
    vat = models.BooleanField(default=False)
    created_by = models.CharField(max_length=50, null=True, blank=True)  # Created By
    TicketID = models.CharField(
        max_length=50, null=True, blank=True
    )  # Associated Ticket ID

    def __str__(self):
        return f"{self.Name} ({self.cashCusID})"

    class Meta:
        db_table = "cash_customer"  # Custom table name
