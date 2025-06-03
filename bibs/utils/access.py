# bibs/utils/access.py

from bibs.models import AccessRights, Menu, Employee  # ensure Employee is imported

def get_employee_menu_names(employee) -> list[str]:
    """Return list of menu names an employee is allowed to see."""
        # ✅ Superuser check
    if getattr(employee, "is_superuser", False):  # or use employee.is_superuser directly
        return list(Menu.objects.values_list("menu_name", flat=True))

    if not employee.nUserRole:
        return []


    # Regular user: return only permitted menus
    menu_ids = (
        AccessRights.objects
        .filter(user_group=employee.nUserRole)
        .values_list('menu_id', flat=True)
        .distinct()
    )
    return list(Menu.objects
                .filter(menu_id__in=menu_ids)
                .values_list('menu_name', flat=True))
