from django.contrib import admin

from .models import CommissionRule, Sale, Seller

admin.site.register(Seller)
admin.site.register(Sale)
admin.site.register(CommissionRule)
