from django.db import models
from django.contrib import auth
from Ecomerce.StoreApp.models import Product

# Create your models here.
class Review(models.Model):
    comment = models.TextField(max_length=500)
    rating = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True, help_text="Date the review was published")
    date_edited = models.DateTimeField(null=True, help_text="Date the review was edited")
    author = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.author