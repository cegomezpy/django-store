from django.db import models
from django.contrib.auth.models import User
from Ecomerce.StoreApp.models import Product

# Create your models here.

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    total_income = models.DecimalField(decimal_places=2, max_digits=10)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} - {self.user} - {self.date_created}"

    def save(self, *args, **kwargs):
        if self.delivered:
            shipping_products = ShippingProducts.objects.filter(shipping=self)
            for shipping_product in shipping_products:
                shipping_product.product.in_stock -= shipping_product.quantity
                shipping_product.product.save()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "shipping"
        ordering = ["date_created"]
        verbose_name = "Shipping"
        verbose_name_plural = "Shippings"


class ShippingProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Product:{self.product.name}Quantity:{self.quantity}UnitaryPrice:{self.product.discount_price}"

    class Meta:
        db_table = "shipping_products"
        ordering = ["id"]
        verbose_name = "ShippingProduct"
        verbose_name_plural = "ShippingProducts"