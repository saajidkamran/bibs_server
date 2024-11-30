from rest_framework import serializers
from .models import (
    MItem,
    MMetal,
    MMetalProcess,
    MProcess,
    MTrsItemsMetals,
    MTrsProcess,
    MTrsMetalMetalProcess,
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


class MMetalSerializer(BaseSerializer):
    class Meta:
        model = MMetal
        fields = "__all__"


class MMetalProcessSerializer(BaseSerializer):
    class Meta:
        model = MMetalProcess
        fields = "__all__"


class MProcessSerializer(BaseSerializer):
    class Meta:
        model = MProcess
        fields = "__all__"


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
