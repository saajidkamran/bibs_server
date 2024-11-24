from rest_framework import serializers
from .models import MItem


class SetupMItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MItem
        fields = "__all__"  # Include all fields
