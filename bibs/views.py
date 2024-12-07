from django.forms import ValidationError
from rest_framework import viewsets, status
from django.db import models  # Import models for aggregate functions
from rest_framework.response import Response
from rest_framework.decorators import action
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
        """
        Generate a unique ID with a specific prefix for the given model and field.
        """
        max_id = model.objects.aggregate(models.Max(field_name))[f"{field_name}__max"]
        print(">> max_id", max_id)
        if max_id:
            # Normalize case for comparison and ensure the format matches the prefix
            if not max_id.upper().startswith(prefix.upper()):
                raise ValueError(f"Invalid max_id format: {max_id}")
            # Extract the numeric part safely
            try:
                numeric_part = int(max_id[len(prefix) :])
            except ValueError:
                raise ValueError(f"Numeric extraction failed for max_id: {max_id}")
            next_id = numeric_part + 1
        else:
            next_id = 1
        # Return the new unique ID with zero-padded numbers
        return f"{prefix.upper()}{next_id:05d}"

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle unique ID generation for new records.
        """
        unique_field_name = self.serializer_class.Meta.unique_field
        unique_field_value = request.data.get(unique_field_name)
        print(">>un", unique_field_name)

        if not unique_field_value:
            # Define prefixes for different unique fields
            prefix_map = {
                "it_id": "itm",
                "met_id": "met",
                "mepr_id": "mpr",
                "pr_id": "prc",
                "nEMPCODE": "emp",
                "nCUSCODE": "cus",
                "nTKTCODE": "tkt",
            }
            prefix = prefix_map.get(unique_field_name, "")
            print(">>prefix", prefix)

            if not prefix:
                raise ValueError(f"No prefix defined for field: {unique_field_name}")

            # Generate the unique ID
            unique_field_value = self.generate_unique_id(
                prefix, self.queryset.model, unique_field_name
            )
            print(">>unique_field_value", unique_field_value)

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

            if request.data.get("nEMPCODE"):
                request.data["nUpdatedBy"] = request.data.pop("user")
            elif request.data.get("nCUSCODE"):
                request.data["nUpdatedBy"] = request.data.pop("user")
            else:
                request.data["updated_by"] = request.data.pop("user")

            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Ensure the 'user' field is provided in the payload
            if "user" not in request.data or not request.data["user"]:
                raise ValidationError({"user": "This field is required for creation."})

            if request.data.get("nEMPCODE"):
                request.data["nCreatedBy"] = request.data.pop("user")
            elif request.data.get("nCUSCODE"):
                request.data["nCreatedBy"] = request.data.pop("user")
            else:
                request.data["created_by"] = request.data.pop("user")

            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Ensure the 'user' field is provided in the payload
        if "user" not in request.data or not request.data["user"]:
            raise ValidationError({"user": "This field is required for updates."})

        if request.data["nEMPCODE"] | request.data["nEMPCODE"]:

            request.data["nUpdatedBy"] = request.data.pop("user")
        else:
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


class MTrsItemsMetalsViewSet(BaseRestrictedViewSet):
    queryset = MTrsItemsMetals.objects.all()
    serializer_class = MTrsItemsMetalsSerializer

    @action(detail=True, methods=["get"], url_path="metals")
    def retrieve_metals(self, request, pk=None):
        """
        Custom endpoint to retrieve all metal IDs (`metal_id`) for a given item ID (`item_id`).
        """
        try:
            item_id = pk  # The item ID passed in the URL
            # Filter using the correct field name: item_id
            related_metals = self.queryset.filter(item_id=item_id).values_list(
                "metal_id", flat=True
            )
            return Response(
                {"met_ids": list(related_metals)}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete-metal")
    def delete_metal(self, request):
        """
        Custom endpoint to delete a specific metal_id associated with an item_id.
        """
        try:
            item_id = request.query_params.get("item_id")
            metal_id = request.query_params.get("metal_id")

            if not item_id or not metal_id:
                return Response(
                    {"error": "Both item_id and metal_id must be provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Filter the specific record
            obj = self.queryset.filter(item_id=item_id, metal_id=metal_id).first()

            if not obj:
                return Response(
                    {"error": "Record not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Delete the record
            obj.delete()
            return Response(
                {
                    "message": f"Metal ID '{metal_id}' successfully deleted for Item ID '{item_id}'."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MTrsProcessViewSet(BaseRestrictedViewSet):
    queryset = MTrsProcess.objects.all()
    serializer_class = MTrsProcessSerializer

    @action(detail=True, methods=["get"], url_path="processes")
    def retrieve_processes(self, request, pk=None):
        """
        Custom endpoint to retrieve all process IDs (`pr_id`) for a given metal ID (`metal_id`).
        """
        try:
            metal_id = pk  # The metal ID passed in the URL
            # Query related processes through metal_process and metal
            related_processes = self.queryset.filter(
                metal_process__mepr_id=metal_id
            ).values_list("process__pr_id", flat=True)

            return Response(
                {"pr_ids": list(related_processes)}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete-metal-process")
    def delete_metal_process(self, request):
        """
        Custom endpoint to delete a specific metal_process associated with a metal.
        """
        try:
            metal_id = request.query_params.get("metal_id")
            metal_process_id = request.query_params.get("metal_process_id")

            if not metal_id or not metal_process_id:
                return Response(
                    {"error": "Both metal_id and metal_process_id must be provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Filter the specific record
            obj = self.queryset.filter(
                metal_process__mepr_id=metal_id, process__pr_id=metal_process_id
            ).first()

            if not obj:
                return Response(
                    {"error": "Record not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Delete the record
            obj.delete()
            return Response(
                {
                    "message": f"Metal process ID '{metal_process_id}' successfully deleted for Metal ID '{metal_id}'."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MTrsMetalMetalProcessViewSet(BaseRestrictedViewSet):
    queryset = MTrsMetalMetalProcess.objects.all()
    serializer_class = MTrsMetalMetalProcessSerializer

    @action(detail=True, methods=["get"], url_path="metal-processes")
    def retrieve_metal_processes(self, request, pk=None):
        """
        Custom endpoint to retrieve all metal-process IDs (`mepr_id`) for a given metal ID (`metal_id`).
        """
        try:
            # Use the primary key (pk) to identify the metal ID
            metal_id = pk  # The metal ID passed in the URL

            # Query the database for related metal processes
            related_metal_processes = self.queryset.filter(
                metal__met_id=metal_id  # Ensure correct field lookup
            ).values_list("metal_process__mepr_id", flat=True)

            # Return the response with the list of related metal process IDs
            return Response(
                {"mepr_ids": list(related_metal_processes)}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete-metal-process")
    def delete_metal_process(self, request):
        """
        Custom endpoint to delete a specific metal_process associated with a metal.
        """
        try:
            metal_id = request.query_params.get("metal_id")
            metal_process_id = request.query_params.get("metal_process_id")

            if not metal_id or not metal_process_id:
                return Response(
                    {"error": "Both metal_id and metal_process_id must be provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Filter the specific record
            obj = self.queryset.filter(
                metal__met_id=metal_id, metal_process__mepr_id=metal_process_id
            ).first()

            if not obj:
                return Response(
                    {"error": "Record not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Delete the record
            obj.delete()
            return Response(
                {
                    "message": f"Metal process ID '{metal_process_id}' successfully deleted for Metal ID '{metal_id}'."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
