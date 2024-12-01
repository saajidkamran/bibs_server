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
from bibs.views import (
    MItemViewSet,
    MMetalViewSet,
    MMetalProcessViewSet,
    MProcessViewSet,
    MTrsItemsMetalsViewSet,
    MTrsProcessViewSet,
    MTrsMetalMetalProcessViewSet,
    EmployeeCreateView,
    CustomerViewSet,
    TicketViewSet,
)

router = DefaultRouter()

# Unrestricted CRUD endpoints
router.register(r"m-items", MItemViewSet)
router.register(r"m-metals", MMetalViewSet)
router.register(r"m-metal-processes", MMetalProcessViewSet)
router.register(r"m-processes", MProcessViewSet)
router.register(
    r"employees",
    EmployeeCreateView,
)  # Employee CRUD ndpoint
router.register(r"customers", CustomerViewSet)
router.register(r"tickets", TicketViewSet)

# Restricted POST/DELETE-only endpoints
router.register(r"trs-items-metals", MTrsItemsMetalsViewSet)
router.register(r"trs-metals-metalprocess", MTrsMetalMetalProcessViewSet)
router.register(r"trs-metalprocess-process", MTrsProcessViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
