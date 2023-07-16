from django.shortcuts import render
from ..models import Product, ProductImage
from django.http import HttpResponseBadRequest
from .ReviewsApp import forms
from .ReviewsApp.models import Review
from django.db.models import Avg
from ..views import annotate_rating

# Create your views here.
def details(request, product_id):
    review_form = forms.ReviewForm()
    if type(product_id) is int:
        # Get reviews related with product
        reviews = Review.objects.filter(product__id=product_id).order_by('id').reverse()
        # Get rating avg and list of stars
        rating_avg = set_average_rating(reviews)
        rating_stars = [float(i) for i in range(1, 6)]
        # Get products and set context
        products = Product.objects.all()
        products = annotate_rating(products)
        product = products.get(id=product_id)
        product_images = ProductImage.objects.filter(product_id=product.id)
        context = {"product":product,
                   "products":products,
                   "product_images":product_images,
                   "review_form":review_form,
                   "reviews":reviews,
                   "rating_stars":rating_stars,
                   "rating_avg":rating_avg
                   }
    else:
        return HttpResponseBadRequest("The id has to be an integer number")
    return render(request, 'details.html', context)

def set_average_rating(reviews):
    # Get rating avg and list of stars
    rating_product_promedy = reviews.aggregate(Avg('rating'))
    if rating_product_promedy['rating__avg']:
        rating_avg = round(rating_product_promedy['rating__avg'], 2)
    else:
        rating_avg = 5
    return rating_avg