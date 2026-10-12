from datetime import date

from django.core.management.base import BaseCommand

from commissions.models import CommissionRule, Sale, Seller


class Command(BaseCommand):
    help = "Crea datos demo para probar la aplicación"

    def handle(self, *args, **options):
        rules = [
            ("Inicial", 0, 0),
            ("Meta bronce", 20, 5),
            ("Meta plata", 50, 8),
            ("Meta oro", 100, 12),
        ]
        for name, minimum, percent in rules:
            CommissionRule.objects.get_or_create(name=name, defaults={"minimum_sales": minimum, "commission_percent": percent})
        sellers = [
            ("Ana Torres", "ana@example.com"),
            ("Luis Mendoza", "luis@example.com"),
            ("Sofía Ruiz", "sofia@example.com"),
        ]
        for name, email in sellers:
            seller, _ = Seller.objects.get_or_create(name=name, defaults={"email": email})
            if not seller.sales.exists():
                Sale.objects.create(seller=seller, amount=25, sale_date=date.today(), description="Venta demo")
        self.stdout.write(self.style.SUCCESS("Datos demo creados."))
