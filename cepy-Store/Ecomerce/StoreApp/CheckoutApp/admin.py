from django.contrib import admin
from .models import Shipping, ShippingProducts

# Register your models here.
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_created', 'total_income', 'delivered')

class ShippingProductsAdmin(admin.ModelAdmin):
    list_display = ('product', 'shipping')

admin.site.register(Shipping, ShippingAdmin)
admin.site.register(ShippingProducts, ShippingProductsAdmin)