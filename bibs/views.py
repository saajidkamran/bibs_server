from rest_framework import viewsets
from .models import MItem
from .serializers import SetupMItemsSerializer
from .models import MMetal
from .serializers import MMetalSerializer
from .models import MMetalProcess
from .serializers import MMetalProcessSerializer


class SetupItemViewSet(viewsets.ModelViewSet):
    queryset = MItem.objects.all()
    serializer_class = SetupMItemsSerializer


class MMetalViewSet(viewsets.ModelViewSet):
    queryset = MMetal.objects.all()  # Fetch all records from MMetal table
    serializer_class = MMetalSerializer  # Use the MMetalSerializer


class MMetalProcessViewSet(viewsets.ModelViewSet):
    queryset = MMetalProcess.objects.all()  # Fetch all records from MMetalProcess table
    serializer_class = MMetalProcessSerializer  # Use the MMetalProcessSerializer
