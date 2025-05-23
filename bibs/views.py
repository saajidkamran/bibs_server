from calendar import month_name
from collections import defaultdict
import datetime
from decimal import Decimal
import json
import os
from PIL import Image
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    CashCustomer,
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
    Menu,
    NPayment,
    NPaymentType,
    SetupCompany,
    Ticket,
    SerialTable,
    NProcessPipeType,
    NProcessType,
    NItemResizeType,
    MTrsProcessType,
    NAccountSummary,
    AccessRights,
    UserGroup,
)
from .serializers import (
    AccessRightsSerializer,
    CashCustomerSerializer,
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
    NPaymentTypeSerializer,
    TicketSerializer,
    NProcessPipeTypeSerializer,
    NProcessTypeSerializer,
    NItemResizeTypeSerializer,
    MTrsProcessTypeSerializer,
    NAccountSummarySerializer,
    CustomTokenObtainPairSerializer,
)


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    A base viewset that enforces:
    - Mandatory 'created_by' when creating a record.
    - Optional 'updated_by' during creation.
    - Mandatory 'updated_by' when updating a record.
    - Optional 'created_by' during updates.
    """

    def generate_unique_id(self, sr_code):
        """
        Generate a unique ID using the count from the SerialTable for the given sr_code.
        """
        try:
            serial_entry = SerialTable.objects.get(sr_code=sr_code)
            current_count = serial_entry.count
            next_id = current_count + 1
            serial_entry.count = next_id  # Increment count in SerialTable
            serial_entry.save()
        except SerialTable.DoesNotExist:
            # If the entry does not exist, create it with count 1
            next_id = 1
            SerialTable.objects.create(
                sr_code=sr_code, count=next_id, description=f"{sr_code} Serial Count"
            )

        # Generate the ID with zero-padded numbers
        return f"{sr_code.upper()}{next_id:05d}"

    def create(self, request, *args, **kwargs):
        """
        Override create method to inject created_by automatically using request.nEmployeeCode.
        """
        unique_field_name = self.serializer_class.Meta.unique_field
        unique_field_value = request.data.get(unique_field_name)

        if not unique_field_value:
            sr_code_map = {
                "it_id": "itm",
                "pt_id": "pt",
                "met_id": "met",
                "mepr_id": "mpr",
                "pr_id": "prc",
                "itmrz_id": "itmrz",
                "nEMPCODE": "emp",
                "nCUSCODE": "cus",
                "nTKTCODE": "tkt",
                "nJOBCODE": "job",
                "cashCusID": "cash",
            }
            sr_code = sr_code_map.get(unique_field_name)
            if not sr_code:
                raise ValueError(
                    f"No serial code defined for field: {unique_field_name}"
                )

            unique_field_value = self.generate_unique_id(sr_code)
            request.data[unique_field_name] = unique_field_value

        # Inject created_by here ✅
        request.data["created_by"] = getattr(request, "nEmployeeCode", None)
        # Check if the record already exists
        instance = self.queryset.filter(
            **{unique_field_name: unique_field_value}
        ).first()

        # if instance:
        # Update existing record

        # if request.data.get("nEMPCODE"):
        #     request.data["nUpdatedBy"] = request.data.pop("user")
        # elif request.data.get("nCUSCODE"):
        #     request.data["nUpdatedBy"] = request.data.pop("user")
        # else:

        # request.data["updated_by"] = getattr(request, "nEmployeeCode", None)

        # serializer = self.get_serializer(instance, data=request.data, partial=False)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        # return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Override update method to inject updated_by automatically using request.nEmployeeCode.
        """
        # Inject updated_by here ✅
        request.data["updated_by"] = getattr(request, "nEmployeeCode", None)

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


class NProcessTypeViewSet(BaseModelViewSet):
    queryset = NProcessType.objects.all()
    serializer_class = NProcessTypeSerializer


class MMetalViewSet(BaseModelViewSet):
    queryset = MMetal.objects.all()
    serializer_class = MMetalSerializer


class MMetalProcessViewSet(BaseModelViewSet):
    queryset = MMetalProcess.objects.all()
    serializer_class = MMetalProcessSerializer


class MProcessViewSet(BaseModelViewSet):
    queryset = MProcess.objects.all()
    serializer_class = MProcessSerializer


class NItemResizeTypeViewSet(BaseModelViewSet):

    queryset = NItemResizeType.objects.all()
    serializer_class = NItemResizeTypeSerializer


class MTrsItemsMetalsViewSet(BaseRestrictedViewSet):
    queryset = MTrsItemsMetals.objects.all()
    serializer_class = MTrsItemsMetalsSerializer

    @action(detail=True, methods=["get"], url_path="metals")
    def retrieve_metals(self, request, pk=None):
        """
        Custom endpoint to retrieve all metal IDs (`metal_id`), sequence numbers (`seq_no`),
        and metal names (`metalName`) for a given item ID (`item_id`).
        """
        try:
            item_id = pk  # The item ID passed in the URL

            # Query related metals from M_trs_items_metals
            related_metals = self.queryset.filter(item_id=item_id).values(
                "metal_id",
                "seq_no",
            )
            # Add the metal name from M_metals for each related metal
            response_data = []
            for metal in related_metals:
                metal_id = metal["metal_id"]
                metal_name = (
                    MMetal.objects.filter(met_id=metal_id)
                    .values_list("desc", flat=True)
                    .first()
                )
                response_data.append(
                    {
                        "met_id": metal_id,
                        "seq_no": metal["seq_no"],
                        "metalName": metal_name,  # Include the metal name
                    }
                )

            return Response(
                {"met_ids": response_data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle updating `seq_no` when provided.
        """
        try:
            item = request.data.get("item")
            metal = request.data.get("metal")
            seq_no = request.data.get("seq_no")

            if not item or not metal:
                return Response(
                    {"error": "Both `item` and `metal` are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if `seq_no` is provided
            if seq_no is not None:
                # Try to find the existing record for the given `item` and `metal`
                instance = self.queryset.filter(item=item, metal=metal).first()

                if instance:
                    # Update the `seq_no` for the specific record
                    instance.seq_no = seq_no
                    instance.save()
                    return Response(
                        {"message": "Sequence number updated successfully."},
                        status=status.HTTP_200_OK,
                    )

            # If no `seq_no` or no matching record, proceed with usual creation
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle updating `seq_no` when provided.
        """
        try:
            process = request.data.get("process")
            metal_process = request.data.get("metal_process")
            seq_no = request.data.get("seq_no")

            if not process or not metal_process:
                return Response(
                    {"error": "Both `process` and `metal_process` are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if `seq_no` is provided
            if seq_no is not None:
                # Try to find the existing record for the given `item` and `metal`
                instance = self.queryset.filter(
                    process=process, metal_process=metal_process
                ).first()

                if instance:
                    # Update the `seq_no` for the specific record
                    instance.seq_no = seq_no
                    instance.save()
                    return Response(
                        {"message": "Sequence number updated successfully."},
                        status=status.HTTP_200_OK,
                    )

            # If no `seq_no` or no matching record, proceed with usual creation
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"], url_path="processes")
    def retrieve_related_processes(self, request, pk=None):
        """
        Retrieve all process IDs and names (`pr_id`, `desc`) related to a given metal-process ID (`mepr_id`).
        """
        try:
            # Use the primary key (pk) to identify the metal-process ID
            metal_process_id = pk

            # Query related processes
            related_processes = self.queryset.filter(
                metal_process_id=metal_process_id
            ).values("process__pr_id", "process__desc", "seq_no")
            response_data = []

            for process in related_processes:
                Process_Pipe = (
                    MProcess.objects.filter(pr_id=process["process__pr_id"])
                    .values_list("pipe", flat=True)
                    .first()
                )

                response_data.append(
                    {
                        "pr_id": process["process__pr_id"],
                        "seq_no": process["seq_no"],
                        "processName": process["process__desc"],
                        "processPipe": Process_Pipe,
                    }
                )
            # Format the response
            # response_data = [
            #     {
            #         "pr_id": process["process__pr_id"],
            #         "seq_no": process["seq_no"],
            #         "processName": process["process__desc"],
            #     }
            #     for process in related_processes
            # ]

            return Response({"process_ids": response_data}, status=status.HTTP_200_OK)
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

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle updating `seq_no` when provided.
        """
        try:
            metal = request.data.get("metal")
            metal_process = request.data.get("metal_process")
            seq_no = request.data.get("seq_no")

            if not metal or not metal_process:
                return Response(
                    {"error": "Both `process` and `metal_process` are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if `seq_no` is provided
            if seq_no is not None:
                # Try to find the existing record for the given `item` and `metal`
                instance = self.queryset.filter(
                    metal=metal, metal_process=metal_process
                ).first()

                if instance:
                    # Update the `seq_no` for the specific record
                    instance.seq_no = seq_no
                    instance.save()
                    return Response(
                        {"message": "Sequence number updated successfully."},
                        status=status.HTTP_200_OK,
                    )

            # If no `seq_no` or no matching record, proceed with usual creation
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"], url_path="metal-processes")
    def retrieve_metalprocess_processes(self, request, pk=None):
        """
        Retrieve all process IDs (`process_id`) and their names for a given metal-process ID (`metal_process_id`).
        """
        try:
            metal_id = pk  # The metal-process ID passed in the URL

            # Query related processes through MTrsProcess
            # Query the related metal processes using the correct field names
            related_metal_processes = self.queryset.filter(metal_id=metal_id).values(
                "metal_process_id", "seq_no"
            )

            # Fetch process names from MProcess table
            response_data = []
            for mProcess in related_metal_processes:
                metal_process_id = mProcess["metal_process_id"]
                mProcess_name = (
                    MMetalProcess.objects.filter(mepr_id=metal_process_id)
                    .values_list("desc", flat=True)
                    .first()
                )
                response_data.append(
                    {
                        "mepr_id": metal_process_id,
                        "seq_no": mProcess["seq_no"],
                        "metalProcessName": mProcess_name,
                    }
                )

            return Response({"processes": response_data}, status=status.HTTP_200_OK)
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


class MTrsProcessTypeViewSet(BaseRestrictedViewSet):
    """
    A ViewSet for managing MTrsProcessType records.
    """

    queryset = MTrsProcessType.objects.all()
    serializer_class = MTrsProcessTypeSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle updating `seq_no` when provided.
        """
        try:
            process_type = request.data.get("process_type")
            process = request.data.get("process")
            seq_no = request.data.get("seq_no")

            if not process_type or not process:
                return Response(
                    {"error": "Both `process_type` and `process` are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if `seq_no` is provided
            if seq_no is not None:
                # Try to find the existing record for the given `process_type` and `process`
                instance = self.queryset.filter(
                    process_type=process_type, process=process
                ).first()

                if instance:
                    # Update the `seq_no` for the specific record
                    instance.seq_no = seq_no
                    instance.save()
                    return Response(
                        {"message": "Sequence number updated successfully."},
                        status=status.HTTP_200_OK,
                    )

            # If no `seq_no` or no matching record, proceed with usual creation
            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"], url_path="related-processes")
    def retrieve_related_processes(self, request, pk=None):
        """
        Retrieve all process IDs (`pr_id`) and their names for a given process type ID (`pt_id`).
        """
        try:
            process_id = pk  # The process type ID passed in the URL
            related_processes_types = self.queryset.filter(
                process_id=process_id
            ).values("process_type_id", "seq_no")

            response_data = []
            for pType in related_processes_types:
                process_ids = pType["process_type_id"]

                Process_name = (
                    NProcessType.objects.filter(pt_id=process_ids)
                    .values_list("processName", flat=True)
                    .first()
                )
                Process_Pipe = (
                    NProcessType.objects.filter(pt_id=process_ids)
                    .values_list("processPipe", flat=True)
                    .first()
                )
                response_data.append(
                    {
                        "pt_id": process_ids,
                        "seq_no": pType["seq_no"],
                        "processName": Process_name,
                    }
                )

            return Response({"processes": response_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["delete"], url_path="delete-process-type")
    def delete_process_type(self, request):
        """
        Custom endpoint to delete a specific process associated with a process type.
        """
        try:
            process_type_id = request.query_params.get("process_type_id")
            process_id = request.query_params.get("process_id")

            if not process_type_id or not process_id:
                return Response(
                    {"error": "Both process_type_id and process_id must be provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Filter the specific record
            obj = self.queryset.filter(
                process_type__pt_id=process_type_id, process__pr_id=process_id
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
                    "message": f"Process ID '{process_id}' successfully deleted for Process Type ID '{process_type_id}'."
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeCreateView(BaseModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Inject custom fields
        data["password"] = make_password("123bibs")
        data["is_first_login"] = True
        data["nActive"] = True

        # Make sure 'user' is included for audit tracking
        if "user" not in data or not data["user"]:
            return Response({"error": "user field is required"}, status=400)

        # Replace request.data with the updated copy before passing to parent create
        request._full_data = data  # override full_data so BaseModelViewSet can use it
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()

        if "password" not in data:
            # If no new password is provided, retain the existing one
            data["password"] = instance.password

        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)



class CustomerViewSet(BaseModelViewSet):
    """
    API endpoint for managing customers.
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        """
        Override the create method to update the NAccountSummary table
        for a newly created customer.
        """
        response = super().create(request, *args, **kwargs)

        # After the customer is created, update NAccountSummary
        customer_data = response.data
        nCUSCODE = customer_data.get("nCUSCODE")
        created_by = customer_data.get("created_by")

        # Check if a record already exists for the customer in NAccountSummary
        if not NAccountSummary.objects.filter(nACUSID=nCUSCODE).exists():
            NAccountSummary.objects.create(
                nACUSID=nCUSCODE,
                nTickets=0,  # Default value
                nPayment=0,  # Default value
                nTotOutStand=0,  # Default value
                created_by=created_by,  # Dynamically set nCreatedBy
            )

        return response

    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to delete the corresponding NAccountSummary
        record when a customer is deleted.
        """
        instance = self.get_object()  # Get the customer instance
        nCUSCODE = instance.nCUSCODE  # Get the customer's nCUSCODE

        # Delete the corresponding record in NAccountSummary
        NAccountSummary.objects.filter(nACUSID=nCUSCODE).delete()

        # Proceed with deleting the customer
        response = super().destroy(request, *args, **kwargs)
        return response


# class TicketViewSet(BaseModelViewSet):
#     """
#     API endpoint for managing tickets.
#     """

#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer


class TicketViewSet(BaseModelViewSet):
    """
    API endpoint for managing tickets.
    """

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        customer_id = data.get("customer")
        # TODO:do it by checking i the cus tabvle if he is vat or not and remove from front end
        is_cash_cus = data.get("isCashCustomer")
        cost_no_vat = data.get("nCostNoVAT")

        # vat_value = 0

        setup_company = SetupCompany.objects.first()
        if is_cash_cus == 2:
            if not setup_company:
                return Response(
                    {"error": "No company found in the SetupCompany table."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        request.data["nCalVat"] = setup_company.vat_no
        request.data["nTCost"] = cost_no_vat
        if is_cash_cus == 2:
            request.data["nTCost"] = cost_no_vat + setup_company.vat_no

        request.data["nTPaid"] = 0
        # check if this neadded and this should be  btcist - ntpaid
        request.data["nTDue"] = cost_no_vat + setup_company.vat_no

        # Ensure the customer field is properly handled
        if customer_id:

            # Check if the customer exists in NAccountSummary
            account_summary = NAccountSummary.objects.filter(
                nACUSID=customer_id
            ).first()
            if account_summary:
                # Update the nTickets value with the nTCost from the ticket
                nTCost = data.get("nTCost", 0)
                if nTCost:
                    account_summary.nTickets += Decimal(nTCost)
                    account_summary.update_outstanding()  # Update nTotOutStand
                    account_summary.save()
                # else:
                #     return Response(
                #         {"error": "nTCost is required and should be a valid number."},
                #         status=status.HTTP_400_BAD_REQUEST,
                #     )

        # Proceed with ticket creation
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["get"], url_path="customer-tickets")
    def get_customer_tickets(self, request):
        """
        Retrieve all tickets for a specific customer based on customer_id.
        """
        customer_id = request.query_params.get("customer_id")
        if not customer_id:
            return Response(
                {"error": "customer_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tickets = self.queryset.filter(customer__nCUSCODE=customer_id)
        if not tickets.exists():
            return Response(
                {"message": f"No tickets found for customer_id '{customer_id}'."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serialized_tickets = self.get_serializer(tickets, many=True)
        return Response(serialized_tickets.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="group-by-month")
    def get_tickets_grouped_by_month(self, request):
        """
        API to retrieve tickets grouped by year and month based on the 'nAcceptedBy' field for a specific customer.
        """
        customer_id = request.query_params.get("customer_id")
        if not customer_id:
            return Response(
                {"error": "customer_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Filter tickets by customer ID
        tickets = self.queryset.filter(customer__nCUSCODE=customer_id)

        if not tickets.exists():
            return Response(
                {"message": "No tickets found for the given customer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Group tickets by year and month
        grouped_tickets = defaultdict(
            lambda: defaultdict(
                lambda: {
                    "no_of_tickets": 0,
                    "job_amount": 0,
                    "paid_amount": 0,
                    "due_amount": 0,
                }
            )
        )

        # Store year-specific totals
        year_totals = defaultdict(
            lambda: {
                "no_of_tickets": 0,
                "job_amount": 0,
                "paid_amount": 0,
                "due_amount": 0,
            }
        )

        for ticket in tickets:
            if ticket.nAcceptedDate:
                try:
                    if isinstance(ticket.nAcceptedDate, datetime.datetime):
                        year = ticket.nAcceptedDate.year
                        month = ticket.nAcceptedDate.month
                    else:
                        continue
                except ValueError:
                    continue

                grouped_tickets[year][month]["no_of_tickets"] += 1
                grouped_tickets[year][month]["job_amount"] += ticket.nTCost
                grouped_tickets[year][month]["paid_amount"] += ticket.nTPaid
                grouped_tickets[year][month]["due_amount"] += ticket.nTDue

                # Update year-specific totals
                year_totals[year]["no_of_tickets"] += 1
                year_totals[year]["job_amount"] += ticket.nTCost
                year_totals[year]["paid_amount"] += ticket.nTPaid
                year_totals[year]["due_amount"] += ticket.nTDue

        # Format the response
        response_data = {}
        for year, months in grouped_tickets.items():
            response_data[year] = {
                "summary": [
                    {
                        "month": month_name[month],
                        "no_of_tickets": data["no_of_tickets"],
                        "job_amount": round(data["job_amount"], 2),
                        "paid_amount": round(data["paid_amount"], 2),
                        "due_amount": round(data["due_amount"], 2),
                    }
                    for month, data in sorted(months.items())
                ],
                "total": {
                    "no_of_tickets": year_totals[year]["no_of_tickets"],
                    "job_amount": round(year_totals[year]["job_amount"], 2),
                    "paid_amount": round(year_totals[year]["paid_amount"], 2),
                    "due_amount": round(year_totals[year]["due_amount"], 2),
                },
            }

        # Calculate overall totals
        total = {
            "no_of_tickets": sum(
                total["no_of_tickets"] for total in year_totals.values()
            ),
            "job_amount": sum(total["job_amount"] for total in year_totals.values()),
            "paid_amount": sum(total["paid_amount"] for total in year_totals.values()),
            "due_amount": sum(total["due_amount"] for total in year_totals.values()),
        }

        return Response(
            {"results": response_data, "overall_total": total},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="settle")
    def settle_due_tickets(self, request):
        """
        Custom action to settle outstanding ticket dues for a customer.
        """
        try:
            # TODO:validate the ustomer by checking if he esisting in database
            # 1. Get input data
            nCusCode = request.data.get("nCusCode")
            cardNumber = request.data.get("cardNumber")  # For paymentType 2
            chequeNumber = request.data.get("chequeNumber")  # For paymentType 3
            docNumber = request.data.get("docNumber")  # For paymentType 3
            bankNumber = request.data.get("bankNumber")  # For paymentType 4
            paymentType = request.data.get("paymentType")
            settlementAmount = Decimal(request.data.get("settlementAmount", 0))
            nEmployeeCode = request.data.get("nEmployeeCode")
            comments = request.data.get("nComments", "")
            if not nCusCode or settlementAmount <= 0:
                return Response(
                    {"error": "Invalid customer code or settlement amount."},
                    status=400,
                )

            if not paymentType:
                return Response({"error": "Payment type is required."}, status=400)

            # 2. Determine paymentDetail based on paymentType
            if paymentType == 2:  # Card payment
                if not cardNumber:
                    return Response(
                        {"error": "Card number is required for paymentType 2 (Card)."},
                        status=400,
                    )
                paymentDetail = f"CRD-{cardNumber}"
            elif paymentType == 3:  # Cheque payment
                if not chequeNumber or not docNumber:
                    return Response(
                        {
                            "error": "Cheque number and doc number are required for paymentType 3 (Cheque)."
                        },
                        status=400,
                    )
                paymentDetail = f"CHK-{chequeNumber} D-{docNumber}"
            elif paymentType == 4:  # Bank payment
                if not bankNumber:
                    return Response(
                        {"error": "Bank number is required for paymentType 4 (Bank)."},
                        status=400,
                    )
                paymentDetail = f"BNK-{bankNumber}"
            else:  # Cash or other payment types
                paymentDetail = "CASH"
            if nCusCode != "CASH":

                # 3. Fetch due tickets for the customer, ordered by oldest nAcceptedDate first
                tickets = Ticket.objects.filter(
                    customer__nCUSCODE=nCusCode, nTDue__gt=0
                ).order_by(
                    "nAcceptedDate", "nTKTCODE"
                )  # Prioritizing oldest ticket first

                if not tickets.exists():
                    return Response(
                        {"message": "No outstanding dues for the customer."}, status=404
                    )

                # 4. Process settlement
                total_settled = Decimal(0)
                for ticket in tickets:
                    due_amount = ticket.nTDue
                    if settlementAmount == 0:
                        break

                    # Deduct from the earliest accepted ticket first
                    payment = min(due_amount, settlementAmount)
                    ticket.nTPaid += payment
                    ticket.nTDue -= payment
                    ticket.save()  # Update ticket table

                    settlementAmount -= payment
                    total_settled += payment

                # 5. Update NAccountSummary
                account_summary = NAccountSummary.objects.filter(
                    nACUSID=nCusCode
                ).first()
                if account_summary:
                    account_summary.nPayment += total_settled
                    account_summary.update_outstanding()  # Recalculate outstanding
                    account_summary.save()

                # 6. Add entry to NPayment
                NPayment.objects.create(
                    nCusID=nCusCode,
                    nMonWeek=0,
                    nPaidAmount=total_settled,
                    nPayType=paymentType,
                    paymentDetail=paymentDetail,
                    nComments=comments,
                    nCreatedDate=datetime.datetime.now(),
                    nCreatedBy=nEmployeeCode,
                )

                # 7. Return response
                return Response(
                    {
                        "message": "Settlement successful.",
                        "total_settled": total_settled,
                        "remaining_amount": settlementAmount,
                        "updated_account_summary": {
                            "nPayment": account_summary.nPayment,
                            "nTotOutStand": account_summary.nTotOutStand,
                        },
                    },
                    status=200,
                )
            else:
                # 1 should check the ticket i d is there in cashccux table
                # 2 update th esettle amount to nTpaid in tickete table
                ticket_id = request.data.get("ticketId")
                # settlementAmount = Decimal(request.data.get("settlementAmount", 0))

                cash_customer = CashCustomer.objects.filter(TicketID=ticket_id).first()
                if not cash_customer:
                    return Response(
                        {"error": "Ticket ID not found in CashCustomer table."},
                        status=404,
                    )

                # Update nTPaid in Ticket table
                ticket = Ticket.objects.filter(nTKTCODE=ticket_id).first()
                if not ticket:
                    return Response({"error": "Ticket not found."}, status=404)

                ticket.nTPaid += settlementAmount
                ticket.save()

                # Add entry to NPayment
                NPayment.objects.create(
                    nCusID=cash_customer.cashCusID,
                    nMonWeek=0,
                    nPaidAmount=settlementAmount,
                    nPayType=paymentType,  # Assuming 1 is for cash payments
                    paymentDetail=paymentDetail,
                    nComments=comments,
                    nCreatedDate=datetime.datetime.now(),
                    nCreatedBy=nEmployeeCode,
                )

                return Response(
                    {
                        "message": "Cash payment settled successfully.",
                        "ticket_id": ticket_id,
                        "nTPaid": ticket.nTPaid,
                        "nCusID": cash_customer.cashCusID,
                    },
                    status=200,
                )

        except Exception as e:
            return Response({"error": str(e)}, status=500)


class JobViewSet(BaseModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        print("image>>", request.FILES.getlist("images"))

        job_code = response.data.get("nJOBCODE")
        images = request.FILES.getlist("images")  # Multiple files
        base_url = request.build_absolute_uri(settings.MEDIA_URL)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        image_data_array = []  # For storing all image dicts

        for image in images:
            ext = image.name.split(".")[-1]
            base_name = f"{timestamp}_{job_code}"

            # RAW
            raw_filename = f"RAW_{base_name}.{ext}"
            raw_rel_path = os.path.join("images/uploads", raw_filename)
            raw_abs_path = os.path.join(settings.MEDIA_ROOT, raw_rel_path)
            os.makedirs(os.path.dirname(raw_abs_path), exist_ok=True)
            with open(raw_abs_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            img = Image.open(image)

            # THUMB
            thumb = img.copy()
            thumb.thumbnail((150, 150))
            thumb_filename = f"THUMB_{base_name}.{ext}"
            thumb_rel_path = os.path.join("images/uploads", thumb_filename)
            thumb_abs_path = os.path.join(settings.MEDIA_ROOT, thumb_rel_path)
            thumb.save(thumb_abs_path)

            # 600x600
            resized = img.copy()
            resized = resized.resize((600, 600))
            resized_filename = f"600_{base_name}.{ext}"
            resized_rel_path = os.path.join("images/uploads", resized_filename)
            resized_abs_path = os.path.join(settings.MEDIA_ROOT, resized_rel_path)
            resized.save(resized_abs_path)

            # Append all URLs to a list
            image_data_array.append(
                {
                    "raw": base_url + raw_rel_path,
                    "thumb": base_url + thumb_rel_path,
                    "600": base_url + resized_rel_path,
                }
            )

        # Save a single JobImage row
        if image_data_array:
            JobImage.objects.create(
                job=Job.objects.get(nJOBCODE=job_code),
                nJOBCODE=job_code,
                img_location=json.dumps(image_data_array),
            )

        return response

    @action(detail=False, methods=["get"], url_path="by-ticket")
    def get_jobs_by_ticket(self, request):
        ticket_id = request.query_params.get("ticket_id")
        if not ticket_id:
            return Response(
                {"error": "ticket_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        jobs = self.queryset.filter(ticket__nTKTCODE=ticket_id)
        if not jobs.exists():
            return Response(
                {"message": f"No jobs found for ticket_id '{ticket_id}'."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobImageViewSet(BaseModelViewSet):
    queryset = JobImage.objects.all()
    serializer_class = JobImageSerializer


class NProcessPipeTypeViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving prototypes.
    """

    queryset = NProcessPipeType.objects.all()
    serializer_class = NProcessPipeTypeSerializer


class NAccountSummaryViewSet(viewsets.ModelViewSet):
    queryset = NAccountSummary.objects.all()
    serializer_class = NAccountSummarySerializer

    # Custom action to filter data based on customer ID
    @action(detail=False, methods=["get"], url_path="by-customer")
    def get_by_customer(self, request):
        customer_id = request.query_params.get("customer_id")
        if not customer_id:
            return Response(
                {"error": "customer_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            account_summaries = self.queryset.filter(nACUSID=customer_id)
            if not account_summaries.exists():
                return Response(
                    {"message": "No account summaries found for the given customer."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(account_summaries, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NPaymentTypeViewSet(ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving payment types.
    """

    queryset = NPaymentType.objects.all()
    serializer_class = NPaymentTypeSerializer


class CashCustomerViewSet(BaseModelViewSet):
    queryset = CashCustomer.objects.all()
    serializer_class = CashCustomerSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create to ensure 'created_by' is properly saved.
        """

        response = super().create(request, *args, **kwargs)  # Save object

        # Debugging log
        print("re>>>ER>>>", request.data)

        return response


class ResetPasswordFirstLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        emp_code = request.data.get("nEMPCODE")
        new_password = request.data.get("password")

        if not emp_code or not new_password:
            return Response(
                {"error": "Both 'nEMPCODE' and 'password' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            employee = Employee.objects.get(nEMPCODE=emp_code)
        except Employee.DoesNotExist:
            return Response(
                {"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if not employee.is_first_login:
            return Response(
                {"error": "Password has already been set."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # ✅ Update to use `password` field
        employee.password = make_password(new_password)
        employee.is_first_login = False
        employee.save(update_fields=["password", "is_first_login"])

        return Response(
            {"message": "Password updated successfully."}, status=status.HTTP_200_OK
        )

class EmailLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = Employee.objects.get(nEmail=email)
        except Employee.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=400)

        # ✅ Update check_password call
        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password"}, status=400)

        refresh = RefreshToken.for_user(user)

        user_role_id = user.nUserRole
        access_rights = AccessRights.objects.filter(user_group=user_role_id)
        menu_ids = access_rights.values_list("menu_id", flat=True).distinct()
        menu_names = list(
            Menu.objects.filter(menu_id__in=menu_ids).values_list("menu_name", flat=True)
        )

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "nEMPCODE": user.nEMPCODE,
                "is_first_login": user.is_first_login,
                "menu_names": menu_names,
            }
        )


class EmailJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise AuthenticationFailed("Email and password required")

        try:
            user = Employee.objects.get(nEmail=email)
        except Employee.DoesNotExist:
            raise AuthenticationFailed("User not found")

        if not user.nPwdHash or not check_password(password, user.nPwdHash):
            raise AuthenticationFailed("Invalid credentials")

        if not user.nActive:
            raise AuthenticationFailed("User is inactive")

        return (user, None)


class AccessRightsViewSet(viewsets.ModelViewSet):
    queryset = AccessRights.objects.all()
    serializer_class = AccessRightsSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Resolve user_group ID
        user_group_name = data.get("user_group")
        try:
            user_group = UserGroup.objects.get(group_name__iexact=user_group_name)
            data["user_group"] = user_group.user_group_id
        except UserGroup.DoesNotExist:
            return Response(
                {"error": f"User group '{user_group_name}' not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Resolve menu ID
        menu_name = data.get("menu")
        try:
            menu = Menu.objects.get(menu_name__iexact=menu_name)
            data["menu"] = menu.menu_id
        except Menu.DoesNotExist:
            return Response(
                {"error": f"Menu '{menu_name}' not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Look up existing AccessRights
        instance = AccessRights.objects.filter(user_group=user_group, menu=menu).first()

        if instance:
            # Update instead of creating a duplicate
            data["updated_by"] = data.pop("user", None)
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new record if not found
        data["created_by"] = data.pop("user", None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def perform_create(self, serializer):
    serializer.save(created_by=self.request.nEmployeeCode)
