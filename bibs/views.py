from rest_framework import viewsets
from .models import MItem
from .serializers import SetupMItemsSerializer


class SetupItemViewSet(viewsets.ModelViewSet):
    queryset = MItem.objects.all()
    serializer_class = SetupMItemsSerializer
