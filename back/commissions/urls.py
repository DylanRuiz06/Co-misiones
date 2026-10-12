from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommissionRuleViewSet, SaleViewSet, SellerViewSet, commission_summary

router = DefaultRouter()
router.register("sellers", SellerViewSet)
router.register("sales", SaleViewSet)
router.register("rules", CommissionRuleViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("commission-summary/", commission_summary, name="commission-summary"),
]
