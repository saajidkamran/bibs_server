from django.forms import ValidationError
from rest_framework import viewsets, status
from django.db import models  # Import models for aggregate functions
from rest_framework.response import Response
from .models import (
    Job,
    JobImage,
    MItem,
    MMetal,
    MMetalProcess,
    MProcess,
    MTrsItemsMetals,
    MTrsMetalMetalProcess,
    MTrsProcess,
    Employee,
    Customer,
    Ticket,
)
from .serializers import (
    JobImageSerializer,
    JobSerializer,
    MItemSerializer,
    MMetalSerializer,
    MMetalProcessSerializer,
    MProcessSerializer,
    MTrsItemsMetalsSerializer,
    MTrsProcessSerializer,
    MTrsMetalMetalProcessSerializer,
    EmployeeSerializer,
    CustomerSerializer,
    TicketSerializer,
)


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    A base viewset that enforces:
    - Mandatory 'created_by' when creating a record.
    - Optional 'updated_by' during creation.
    - Mandatory 'updated_by' when updating a record.
    - Optional 'created_by' during updates.
    """

    def generate_unique_id(self, prefix, model, field_name):
        # Get the current maximum ID for the field
        max_id = model.objects.aggregate(models.Max(field_name))[f"{field_name}__max"]
        if max_id:
            # Extract numeric part and increment it
            numeric_part = int(max_id.replace(prefix, ""))
            next_id = numeric_part + 1
        else:
            next_id = 1
        return f"{prefix}{next_id:05d}"

    def create(self, request, *args, **kwargs):
        unique_field_name = self.serializer_class.Meta.unique_field
        unique_field_value = request.data.get(unique_field_name)

        if not unique_field_value:
            # Determine the prefix based on the model
            prefix = ""
            if unique_field_name == "it_id":
                prefix = "itm"
            elif unique_field_name == "met_id":
                prefix = "met"
            elif unique_field_name == "mepr_id":
                prefix = "mpr"
            elif unique_field_name == "pr_id":
                prefix = "prc"
            # Add other cases if needed

            # Generate the unique ID
            unique_field_value = self.generate_unique_id(
                prefix, self.queryset.model, unique_field_name
            )
            request.data[unique_field_name] = unique_field_value

        # Check if the record already exists
        instance = self.queryset.filter(
            **{unique_field_name: unique_field_value}
        ).first()

        if instance:
            # Update existing record
            if "user" not in request.data or not request.data["user"]:
                raise ValidationError(
                    {"updated_by": "This field is required for updates."}
                )
            request.data["updated_by"] = request.data.pop("user")

            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Ensure the 'user' field is provided in the payload
            if "user" not in request.data or not request.data["user"]:
                raise ValidationError({"user": "This field is required for creation."})

            # Map 'user' to 'created_by'
            request.data["created_by"] = request.data.pop("user")

            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Ensure the 'user' field is provided in the payload
        if "user" not in request.data or not request.data["user"]:
            raise ValidationError({"user": "This field is required for updates."})

        # Map 'user' to 'updated_by'
        request.data["updated_by"] = request.data.pop("user")

        return super().update(request, *args, **kwargs)


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


class EmployeeCreateView(BaseModelViewSet):
    """
    API view to create or update an employee based on nEMPCODE.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class CustomerViewSet(BaseModelViewSet):
    """
    API endpoint for managing customers.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class TicketViewSet(BaseModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class JobViewSet(BaseModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobImageViewSet(BaseModelViewSet):
    queryset = JobImage.objects.all()
    serializer_class = JobImageSerializer
