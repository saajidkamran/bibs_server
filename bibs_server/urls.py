from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bibs.views import (
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
)
from django.conf import settings
from django.conf.urls.static import static

# DRF Router
router = DefaultRouter()

router.register(r"m-items", MItemViewSet)
router.register(r"m-metals", MMetalViewSet)
router.register(r"m-metal-processes", MMetalProcessViewSet)
router.register(r"prototypes-list", NProcessPipeTypeViewSet)
router.register(r"m-processes", MProcessViewSet)
router.register(r"m-process-types", NProcessTypeViewSet)
router.register(r"m-item-resize", NItemResizeTypeViewSet)

router.register(r"employees", EmployeeCreateView)
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

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
