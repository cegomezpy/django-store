from django.shortcuts import render
from ..models import Product, ProductImage, Events, EventsImages
from django.http import HttpResponseBadRequest
#from .ReviewsApp import forms
#from .ReviewsApp.models import Review
from django.db.models import Avg
#from ..views import annotate_rating

# Create your views here.
def details(request, header, product_id):
    #review_form = forms.ReviewForm()
    if type(product_id) is int:
        condition = header == "products"
        # Get reviews related with product
        #reviews = Review.objects.filter(product__id=product_id).order_by('id').reverse()
        # Get rating avg and list of stars
        #rating_avg = set_average_rating(reviews)
        #rating_stars = [float(i) for i in range(1, 6)]
        # Get query and set context
        query = Product.objects.all() if condition else Events.objects.all()
        #query = annotate_rating(query)
        product = query.get(id=product_id)
        query_images =ProductImage.objects.filter(product_id=product.id) if condition else EventsImages.objects.filter(event_id=product.id)
        context = {"header":header,
                   "product":product,
                   "products":query,
                   "products_images":query_images,
                   #"review_form":review_form,
                   #"reviews":reviews,
                   #"rating_stars":rating_stars,
                   #"rating_avg":rating_avg
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