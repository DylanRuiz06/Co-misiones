from rest_framework import serializers

from .models import CommissionRule, Sale, Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["id", "name", "email", "active", "created_at"]
        read_only_fields = ["id", "created_at"]


class SaleSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(source="seller.name", read_only=True)

    class Meta:
        model = Sale
        fields = ["id", "seller", "seller_name", "amount", "sale_date", "description", "created_at"]
        read_only_fields = ["id", "seller_name", "created_at"]


class CommissionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionRule
        fields = ["id", "name", "minimum_sales", "commission_percent", "active"]
        read_only_fields = ["id"]
