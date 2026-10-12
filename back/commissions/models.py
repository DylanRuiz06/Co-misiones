from django.core.validators import MinValueValidator
from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "vendedor"
        verbose_name_plural = "vendedores"

    def __str__(self):
        return self.name


class Sale(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="sales")
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    sale_date = models.DateField()
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-sale_date", "-id"]
        verbose_name = "venta"
        verbose_name_plural = "ventas"

    def __str__(self):
        return f"{self.seller.name} - {self.amount}"


class CommissionRule(models.Model):
    name = models.CharField(max_length=120)
    minimum_sales = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["minimum_sales"]
        verbose_name = "regla de comisión"
        verbose_name_plural = "reglas de comisión"

    def __str__(self):
        return f"{self.name} ({self.commission_percent}%)"
