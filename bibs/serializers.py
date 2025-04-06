from rest_framework import serializers
from .models import (
    JobImage,
    MItem,
    MMetal,
    MMetalProcess,
    MProcess,
    MTrsItemsMetals,
    MTrsProcess,
    MTrsMetalMetalProcess,
    Employee,
    Customer,
    NPaymentType,
    Ticket,
    Job,
    NProcessType,
    NItemResizeType,
    MTrsProcessType,
    NProcessPipeType,
    NAccountSummary,
    CashCustomer,
)


class BaseSerializer(serializers.ModelSerializer):
    """
    A base serializer to enforce 'updated_by' validation during updates.
    """

    def validate(self, data):
        if self.instance:
            # Validation for updates
            # if "updated_by" not in data or not data["updated_by"]:
            #     raise serializers.ValidationError(
            #         {"updated_by": "This field is required for updates."}
            #     )
            # else:
            # Validation for creation
            if "created_by" not in data or not data["created_by"]:
                raise serializers.ValidationError(
                    {"created_by": "This field is required for creation."}
                )
        return data


class MItemSerializer(BaseSerializer):
    class Meta:
        model = MItem
        fields = "__all__"
        unique_field = "it_id"


class MMetalSerializer(BaseSerializer):
    class Meta:
        model = MMetal
        fields = "__all__"
        unique_field = "met_id"


class MMetalProcessSerializer(BaseSerializer):
    class Meta:
        model = MMetalProcess
        fields = "__all__"
        unique_field = "mepr_id"


class MProcessSerializer(BaseSerializer):
    class Meta:
        model = MProcess
        fields = "__all__"
        unique_field = "pr_id"


class MTrsItemsMetalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MTrsItemsMetals
        fields = "__all__"


class MTrsMetalMetalProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = MTrsMetalMetalProcess
        fields = "__all__"


class MTrsProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = MTrsProcess
        fields = "__all__"


class MTrsProcessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MTrsProcessType
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"  # Include all fields
        unique_field = "nEMPCODE"

        extra_kwargs = {
            "nId": {"read_only": True},  # nId is auto-generated, so make it read-only
            "nEMPCODE": {"required": False},
            "nUserRole": {"required": True},
            "nActive": {"required": True},
            "nFirstName": {"required": True},
            "nSurName": {"required": True},
            "nAddress1": {"required": True},
            "nAddress2": {"required": False},
            "nAddress3": {"required": False},
            "nTown": {"required": True},
            "nPostCode": {"required": True},
            "nPhone": {"required": True},
            "nMobile": {"required": True},
            "nEmail": {"required": True},
            "nBasicSal": {"required": True},
            "nOverTime": {"required": True},
            "nNoOfAppLeave": {"required": False},
            "nLeaveTaken": {"required": False},
            "created_by": {"required": False},
            "nUpdatedBy": {"required": False},
            "nPwdHash": {"required": False},
            "nPwdSalt": {"required": False},
        }


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        unique_field = "nCUSCODE"

        extra_kwargs = {
            "nCUSCODE": {"required": True},
            "nCTId": {"required": False},
            "nActive": {"required": True},
            "nComName": {"required": True},
            "nSurName": {"required": True},
            "nFirstName": {"required": True},
            "nAddress1": {"required": True},
            "nAddress2": {"required": False},
            "nAddress3": {"required": False},
            "nCity": {"required": True},
            "nState": {"required": False},
            "nPostCode": {"required": True},
            "nPhone1": {"required": True},
            "nPhone2": {"required": True},
            "nMobile": {"required": True},
            "nFax": {"required": True},
            "nEmail": {"required": True},
            "nWebsite": {"required": True},
            "nCreditLimit": {"required": True},
            "nVAT": {"required": True},
            "created_by": {"required": False},
            "nUpdatedBy": {"required": False},
            "nSMS": {"required": True},
        }


class NAccountSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = NAccountSummary
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        unique_field = "nTKTCODE"

    def validate_customer(self, value):
        if value == "":
            return None  # Convert empty string to None
        return value


class JobImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobImage
        fields = "__all__"
        unique_field = "img_id"


class JobSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = "__all__"  # or list fields manually
        unique_field = "nJOBCODE"

    def get_images(self, obj):
        return [image.img_location for image in obj.images.all()]


class NProcessPipeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NProcessPipeType
        fields = ["nPTId", "nProType"]


class NProcessTypeSerializer(BaseSerializer):
    class Meta:
        model = NProcessType
        fields = "__all__"
        unique_field = "pt_id"


class NItemResizeTypeSerializer(BaseSerializer):
    class Meta:
        model = NItemResizeType
        fields = "__all__"
        unique_field = "itmrz_id"


class NPaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPaymentType
        fields = "__all__"  # Serialize all fields


class CashCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashCustomer
        fields = "__all__"  # Serialize all fields
        unique_field = "cashCusID"
