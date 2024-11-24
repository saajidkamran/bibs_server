from rest_framework import serializers
from .models import MItem
from .models import MMetal
from .models import MMetalProcess


class SetupMItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MItem
        fields = "__all__"  # Include all fields


class MMetalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MMetal
        fields = "__all__"  # Include all fields in the API


class MMetalProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = MMetalProcess
        fields = "__all__"  # Include all fields in the API
