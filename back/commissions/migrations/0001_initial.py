from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Seller",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["name"], "verbose_name": "vendedor", "verbose_name_plural": "vendedores"},
        ),
        migrations.CreateModel(
            name="CommissionRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("minimum_sales", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ("commission_percent", models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0)])),
                ("active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["minimum_sales"], "verbose_name": "regla de comisión", "verbose_name_plural": "reglas de comisión"},
        ),
        migrations.CreateModel(
            name="Sale",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ("sale_date", models.DateField()),
                ("description", models.CharField(blank=True, max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("seller", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sales", to="commissions.seller")),
            ],
            options={"ordering": ["-sale_date", "-id"], "verbose_name": "venta", "verbose_name_plural": "ventas"},
        ),
    ]
