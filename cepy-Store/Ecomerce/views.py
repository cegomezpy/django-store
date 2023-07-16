# Import the necessary modules
from django.db.models import Count
from django.shortcuts import render
from .StoreApp.models import Product, Category
from .StoreApp.views import annotate_rating

def index(request):
    # Get all products with a discount greater than or equal to 20%
    discount_products = Product.objects.filter(discount__gte=20)

    # Get all products that are in stock (quantity less than or equal to 5)
    in_stock_products = Product.objects.filter(in_stock__lte=5)

    # Annotate rating
    discount_products = annotate_rating(discount_products)
    in_stock_products = annotate_rating(in_stock_products)
    # Get the number of products in each category
    categories = Category.objects.all().annotate(quantity=Count("products"))

    # Define the context data to pass to the template
    context = {
        "discount_products": discount_products,
        "in_stock_products": in_stock_products,
        "categories": categories,
        "rating_stars":[1, 2, 3, 4, 5]
    }

    # Render the index template with the context data
    return render(request, 'index.html', context)