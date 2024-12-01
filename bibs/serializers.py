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
    Ticket,
    Job,
)


class BaseSerializer(serializers.ModelSerializer):
    """
    A base serializer to enforce 'updated_by' validation during updates.
    """

    def validate(self, data):
        if self.instance and "updated_by" not in data:
            raise serializers.ValidationError(
                {"updated_by": "This field is required for updates."}
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


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"  # Include all fields
        unique_field = "nEMPCODE"

        extra_kwargs = {
            "nId": {"read_only": True},  # nId is auto-generated, so make it read-only
            "nEMPCODE": {"required": True},
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
            "nNoOfAppLeave": {"required": True},
            "nLeaveTaken": {"required": True},
            "nCreatedBy": {"required": False},
            "nUpdatedBy": {"required": False},
            "nPwdHash": {"required": True},
            "nPwdSalt": {"required": True},
        }


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        unique_field = "nCUSCODE"

        extra_kwargs = {
            "nCUSCODE": {"required": True},
            "nCTId": {"required": True},
            "nActive": {"required": True},
            "nComName": {"required": True},
            "nSurName": {"required": True},
            "nFirstName": {"required": True},
            "nAddress1": {"required": True},
            "nAddress2": {"required": False},
            "nAddress3": {"required": False},
            "nCity": {"required": True},
            "nState": {"required": True},
            "nPostCode": {"required": True},
            "nPhone1": {"required": True},
            "nPhone2": {"required": True},
            "nMobile": {"required": True},
            "nFax": {"required": True},
            "nEmail": {"required": True},
            "nWebsite": {"required": True},
            "nCreditLimit": {"required": True},
            "nVAT": {"required": True},
            "nCreatedBy": {"required": False},
            "nUpdatedBy": {"required": False},
            "nSMS": {"required": True},
        }


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        unique_field = "nTKTCODE"


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        unique_field = "nJOBCODE"


class JobImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobImage
        fields = "__all__"
        unique_field = "img_id"
