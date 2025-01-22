from decimal import ROUND_HALF_UP, Decimal
from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
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
    SetupCompany,
    Ticket,
    SerialTable,
    NProcessPipeType,
    NProcessType,
    NItemResizeType,
    MTrsProcessType,
    NAccountSummary,
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
    NProcessPipeTypeSerializer,
    NProcessTypeSerializer,
    NItemResizeTypeSerializer,
    MTrsProcessTypeSerializer,
    NAccountSummarySerializer,
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
        Override the create method to handle unique ID generation for new records.
        """
        unique_field_name = self.serializer_class.Meta.unique_field
        unique_field_value = request.data.get(unique_field_name)
        if not request.data.get(unique_field_name):
            # Define prefixes for different sr_codes
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
            }
            sr_code = sr_code_map.get(unique_field_name)
            if not sr_code:
                raise ValueError(
                    f"No serial code defined for field: {unique_field_name}"
                )

            # Generate the unique ID
            unique_field_value = self.generate_unique_id(sr_code)
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

            # if request.data.get("nEMPCODE"):
            #     request.data["nUpdatedBy"] = request.data.pop("user")
            # elif request.data.get("nCUSCODE"):
            #     request.data["nUpdatedBy"] = request.data.pop("user")
            # else:

            request.data["updated_by"] = request.data.pop("user")

            serializer = self.get_serializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Ensure the 'user' field is provided in the payload
            if "user" not in request.data or not request.data["user"]:
                raise ValidationError({"user": "This field is required for creation."})

            # if request.data.get("nEMPCODE"):
            #     request.data["nCreatedBy"] = request.data.pop("user")
            # elif request.data.get("nCUSCODE"):
            #     request.data["nCreatedBy"] = request.data.pop("user")
            # else:
            request.data["created_by"] = request.data.pop("user")

            return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Ensure the 'user' field is provided in the payload
        if "user" not in request.data or not request.data["user"]:
            raise ValidationError({"user": "This field is required for updates."})

        # if request.data["nEMPCODE"] | request.data["nEMPCODE"]:

        #     request.data["nUpdatedBy"] = request.data.pop("user")
        # else:

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
        price_no_vat = data.get("nCostNoVAT")
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
            # Add the latest vat_no to the ticket data
            # vat_value = (setup_company.vat_no * price_no_vat / Decimal(100)).quantize(
            #     Decimal("0.01"), ROUND_HALF_UP
            # )

        request.data["nCalVat"] = setup_company.vat_no
        request.data["nTCost"] = cost_no_vat + setup_company.vat_no
        request.data["nTPaid"] = 0
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
                else:
                    return Response(
                        {"error": "nTCost is required and should be a valid number."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

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


class JobViewSet(BaseModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


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
