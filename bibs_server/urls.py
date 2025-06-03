"""
URL configuration for bibs_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from bibs.views import (
    AccessRightsUpsertAPIView,
    CashCustomerViewSet,
    JobImageViewSet,
    JobViewSet,
    MItemViewSet,
    MMetalViewSet,
    MMetalProcessViewSet,
    MProcessViewSet,
    MTrsItemsMetalsViewSet,
    MTrsProcessViewSet,
    MTrsMetalMetalProcessViewSet,
    EmployeeCreateView,
    CustomerViewSet,
    NPaymentTypeViewSet,
    TicketViewSet,
    NProcessPipeTypeViewSet,
    NProcessTypeViewSet,
    NItemResizeTypeViewSet,
    MTrsProcessTypeViewSet,
    NAccountSummaryViewSet,
    ResetPasswordFirstLoginView,
    EmailLoginView,
    UserGroupViewSet,
    MenuViewSet
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


router = DefaultRouter()

# Unrestricted CRUD endpoints
router.register(r"m-items", MItemViewSet)
router.register(r"m-metals", MMetalViewSet)
router.register(r"m-metal-processes", MMetalProcessViewSet)
router.register(r"prototypes-list", NProcessPipeTypeViewSet)
router.register(r"m-processes", MProcessViewSet)
router.register(r"m-process-types", NProcessTypeViewSet)
router.register(r"m-item-resize", NItemResizeTypeViewSet)


router.register(r"employees", EmployeeCreateView)  # Employee CRUD ndpoint
router.register(r"customers", CustomerViewSet)
router.register(r"tickets", TicketViewSet)
router.register(r"jobs", JobViewSet)
router.register(r"job-images", JobImageViewSet)

router.register(r"trs-items-metals", MTrsItemsMetalsViewSet)
router.register(r"trs-metals-metalprocess", MTrsMetalMetalProcessViewSet)
router.register(r"trs-metalprocess-process", MTrsProcessViewSet)
router.register(r"trs-process-types", MTrsProcessTypeViewSet)
router.register(r"naccountsummary", NAccountSummaryViewSet, basename="naccountsummary")
router.register(r"cash-customers", CashCustomerViewSet, basename="cash-customer")
router.register(r"payment-types", NPaymentTypeViewSet)
router.register(r"user-groups", UserGroupViewSet, basename="usergroup")
router.register(r"menus", MenuViewSet, basename="menu")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # Custom endpoints
    path("api/access-rights/upsert/", AccessRightsUpsertAPIView.as_view(), name="access-rights-upsert"),
    path("api/reset-password/", ResetPasswordFirstLoginView.as_view(), name="reset-password"),
    path("api/login/", EmailLoginView.as_view(), name="email-login"),

    # JWT-specific
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
