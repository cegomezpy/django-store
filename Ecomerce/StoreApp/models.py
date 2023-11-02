from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to="Categories")
    image_thumbnail = ImageSpecField(source='image', processors=[Thumbnail(500, 500)], format='JPEG', options={'quality': 20})

    def __str__(self):
        return self.name

class AbstractProducts(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    default_image = models.ImageField(upload_to="ProductsImages")
    default_image_thumbnail = ImageSpecField(source='default_image', processors=[Thumbnail(500, 500)], format='JPEG', options={'quality': 20})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.discount:
            self.discount_price = self.price * (1 - self.discount/100)
        else:
            self.discount_price = self.price
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

class AbstractImages(models.Model):
    image = models.ImageField(upload_to='Images')

    class Meta:
        abstract = True

class Product(AbstractProducts):
    in_stock = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name='products')
    def save(self, *args, **kwargs):
        if self.in_stock <= 0:
            self.available = False
        super().save(*args, **kwargs)
        if not ProductImage.objects.filter(image=self.default_image).exists():
            product_image = ProductImage(product=self, image=self.default_image)
            product_image.save()

class Events(AbstractProducts):
    categories = models.ManyToManyField(Category, related_name='events')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not EventsImages.objects.filter(image=self.default_image).exists():
            product_image = EventsImages(event=self, image=self.default_image)
            product_image.save()

class ProductImage(AbstractImages):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products")
    def __str__(self):
        return self.product.name

class EventsImages(AbstractImages):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name="events")
    def __str__(self):
        return self.event.name