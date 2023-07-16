from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="Categories")
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(500, 500)],
                                      format='JPEG',
                                      options={'quality': 20})

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    default_image = models.ImageField(upload_to="ProductsImages")
    default_image_thumbnail = ImageSpecField(source='default_image',
                                      processors=[ResizeToFill(500, 500)],
                                      format='JPEG',
                                      options={'quality': 20})
    in_stock = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not ProductImage.objects.filter(image=self.default_image).exists():
            product_image = ProductImage(product=self, image=self.default_image)
            product_image.save()
        if self.in_stock <= 0:
            self.available = False
        if self.discount:
            self.discount_price = self.price * (1 - self.discount/100)
        else:
            self.discount_price = self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ProductsImages')
    def __str__(self):
        return self.product.name + ' Image'