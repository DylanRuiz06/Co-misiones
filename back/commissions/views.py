from datetime import date
from decimal import Decimal

from django.db.models import Sum
from django.utils.dateparse import parse_date
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CommissionRule, Sale, Seller
from .serializers import CommissionRuleSerializer, SaleSerializer, SellerSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.select_related("seller").all()
    serializer_class = SaleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        seller_id = self.request.query_params.get("seller")
        start_date = parse_date(self.request.query_params.get("start_date", ""))
        end_date = parse_date(self.request.query_params.get("end_date", ""))
        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)
        if start_date:
            queryset = queryset.filter(sale_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(sale_date__lte=end_date)
        return queryset


class CommissionRuleViewSet(viewsets.ModelViewSet):
    queryset = CommissionRule.objects.all()
    serializer_class = CommissionRuleSerializer


@api_view(["GET"])
def commission_summary(request):
    start_date = parse_date(request.query_params.get("start_date", ""))
    end_date = parse_date(request.query_params.get("end_date", ""))
    if not start_date or not end_date:
        return Response({"detail": "start_date y end_date son obligatorias (YYYY-MM-DD)."}, status=status.HTTP_400_BAD_REQUEST)
    if start_date > end_date:
        return Response({"detail": "start_date no puede ser posterior a end_date."}, status=status.HTTP_400_BAD_REQUEST)

    seller_id = request.query_params.get("seller")
    sellers = Seller.objects.filter(active=True)
    if seller_id:
        sellers = sellers.filter(id=seller_id)
    rules = list(CommissionRule.objects.filter(active=True).order_by("-minimum_sales"))
    result = []
    for seller in sellers:
        total = seller.sales.filter(sale_date__range=(start_date, end_date)).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        rule = next((candidate for candidate in rules if total >= candidate.minimum_sales), None)
        percent = rule.commission_percent if rule else Decimal("0")
        commission = (total * percent / Decimal("100")).quantize(Decimal("0.01"))
        result.append({
            "seller_id": seller.id,
            "seller_name": seller.name,
            "total_sales": total,
            "rule_id": rule.id if rule else None,
            "rule_name": rule.name if rule else "Sin regla alcanzada",
            "commission_percent": percent,
            "commission": commission,
        })
    return Response({"start_date": start_date, "end_date": end_date, "results": result})
