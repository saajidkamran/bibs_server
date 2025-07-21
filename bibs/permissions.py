from rest_framework.permissions import BasePermission
from bibs.models import AccessRights, Menu, Employee

SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]
# permissions.py
class HasAccessRight(BasePermission):
    def has_permission(self, request, view):
        # 1️⃣ super-user short-circuit
        if hasattr(request.user, "nEMPCODE"):
            try:
                employee = Employee.objects.get(nEMPCODE=request.user.nEMPCODE)

                if employee.is_superuser:
                    return True
            except Employee.DoesNotExist:
                return False

        # 2️⃣ accept either a single str or a list/tuple of str
        raw_codes = getattr(view, "menu_code", None)
        if not raw_codes:
            return False
        menu_codes = (
            [raw_codes] if isinstance(raw_codes, str) else list(raw_codes)
        )

        # 3️⃣ look-up all matching Menu rows in one query
        menus = (
            Menu.objects.filter(menu_name__in=menu_codes)
            .values_list("menu_id", flat=True)
        )
        if not menus:
            return False

        user_group_id = getattr(request.user, "nUserRole", None)
        if user_group_id is None:
            return False

        # 4️⃣ any AccessRights row that matches ⇒ success
        access = AccessRights.objects.filter(
            menu_id__in=menus, user_group_id=user_group_id
        ).first()
        if not access:
            return False

        method = request.method
        if method in SAFE_METHODS:
            return access.view
        if method == "POST":
            return access.add
        if method in ["PUT", "PATCH"]:
            return access.update
        if method == "DELETE":
            return access.delete
        return False
