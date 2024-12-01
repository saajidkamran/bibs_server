from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .models import (
    MItem,
    MMetal,
    MMetalProcess,
    MProcess,
    MTrsItemsMetals,
    MTrsMetalMetalProcess,
    MTrsProcess,
    Employee,
)
from .serializers import (
    MItemSerializer,
    MMetalSerializer,
    MMetalProcessSerializer,
    MProcessSerializer,
    MTrsItemsMetalsSerializer,
    MTrsProcessSerializer,
    MTrsMetalMetalProcessSerializer,
    EmployeeSerializer,
)


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    A base viewset that enforces:
    1. Custom delete responses.
    2. Validation for mandatory 'updated_by' field.
    3. Upsert behavior on create.
    """

    def create(self, request, *args, **kwargs):
        # Get the unique identifier for upsert logic (defined in each serializer)
        unique_field_name = self.serializer_class.Meta.unique_field
        unique_field_value = request.data.get(unique_field_name)

        if not unique_field_value:
            return Response(
                {unique_field_name: f"{unique_field_name} is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the record exists
        instance = self.queryset.filter(
            **{unique_field_name: unique_field_value}
        ).first()

        if instance:
            # Update the existing record
            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Create a new record
            return super().create(request, *args, **kwargs)


class BaseRestrictedViewSet(viewsets.ModelViewSet):
    """
    A base viewset for restricted behavior:
    - Allows only POST and DELETE.
    - Disallows GET, PUT, and PATCH.
    """

    def list(self, request, *args, **kwargs):
        return Response(
            {"error": "GET method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"error": "GET method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "PUT method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"error": "PATCH method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )


# Full CRUD for Standard Tables
class MItemViewSet(BaseModelViewSet):
    queryset = MItem.objects.all()
    serializer_class = MItemSerializer


class MMetalViewSet(BaseModelViewSet):
    queryset = MMetal.objects.all()
    serializer_class = MMetalSerializer


class MMetalProcessViewSet(BaseModelViewSet):
    queryset = MMetalProcess.objects.all()
    serializer_class = MMetalProcessSerializer


class MProcessViewSet(BaseModelViewSet):
    queryset = MProcess.objects.all()
    serializer_class = MProcessSerializer


# Restricted API for TRS Tables
class MTrsItemsMetalsViewSet(BaseRestrictedViewSet):
    queryset = MTrsItemsMetals.objects.all()
    serializer_class = MTrsItemsMetalsSerializer


class MTrsProcessViewSet(BaseRestrictedViewSet):
    queryset = MTrsProcess.objects.all()
    serializer_class = MTrsProcessSerializer


class MTrsMetalMetalProcessViewSet(BaseRestrictedViewSet):
    queryset = MTrsMetalMetalProcess.objects.all()
    serializer_class = MTrsMetalMetalProcessSerializer


class EmployeeCreateView(viewsets.ModelViewSet):
    """
    API view to create or update an employee based on nEMPCODE.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        # Extract the unique identifier (e.g., nEMPCODE) from the request data
        nEMPCODE = request.data.get("nEMPCODE")

        # Check if an employee with the same nEMPCODE exists
        employee = Employee.objects.filter(nEMPCODE=nEMPCODE).first()

        if employee:
            # If exists, update the employee
            serializer = self.get_serializer(employee, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If not, create a new employee
            return super().create(request, *args, **kwargs)
