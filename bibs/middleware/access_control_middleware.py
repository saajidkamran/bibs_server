from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from bibs.models import Employee, AccessRights, Menu
from django.urls import resolve

class AccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #  Paths that should skip auth and access control for all methods
        white_list_paths = [
            "/api/login/",
            "/api/token/refresh/",
            "/api/token/verify/",
            "/api/trs-items-metals/",
            "/api/m-processes//",
            "/api/m-processes/",
            "/api/m-metal-processes/",
            "/api/naccountsummary/",
            "/api/tickets/customer-tickets/",
            "/api/trs-metalprocess-process/",
            "/api/trs-metals-metalprocess/",
            "/api/payment-types/",
            "/api/cash-customers/",
            "/api/job-images/",
            "/api/jobs/",
            "/api/prototypes-list/",
            "/api/m-process-types/",
            "/api/customers/",
            "/api/tickets/",
            "/api/tickets/group-by-month/",
            "/media/images/uploads/"
        ]

        # Skip middleware for any matching exempt path prefix
        if any(request.path.startswith(p) for p in white_list_paths):
            return self.get_response(request)

        try:
            # Step 1: Extract Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return JsonResponse({"error": "Authorization header missing."}, status=403)

            # Step 2: Extract token
            token = auth_header.split(" ")[1]

            # Step 3: Validate token
            user_auth = JWTAuthentication()
            validated_token = user_auth.get_validated_token(token)
            nEMPCODE = validated_token["nEMPCODE"]
            request.nEmployeeCode = nEMPCODE  #  Inject employee code into request

            # Step 4: Access control
            employee = Employee.objects.get(nEMPCODE=nEMPCODE)
            user_role = employee.nUserRole

            resolver_match = resolve(request.path)
            route_parts = resolver_match.route.split("/")
            menu_name = route_parts[1] if len(route_parts) > 1 else ""
            menu = Menu.objects.filter(menu_name__iexact=menu_name).first()
            if not menu:
                return JsonResponse({"error": "Menu not found."}, status=403)

            access_right = AccessRights.objects.filter(
                user_group=user_role,
                menu=menu.menu_id,
            ).first()

            if not access_right:
                return JsonResponse({"error": "Access denied."}, status=403)

            method = request.method
            if method == "POST" and not access_right.add:
                return JsonResponse({"error": "No Add Permission."}, status=403)
            if method in ["PUT", "PATCH"] and not (access_right.edit or access_right.update):
                return JsonResponse({"error": "No Edit/Update Permission."}, status=403)
            if method == "DELETE" and not access_right.delete:
                return JsonResponse({"error": "No Delete Permission."}, status=403)

            return self.get_response(request)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=403)
