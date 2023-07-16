from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from Ecomerce.StoreApp.models import Product
from .models import Review
from .forms import ReviewForm
from django.http import JsonResponse, HttpResponse
import datetime

# Create your views here.
@login_required
def review(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        print(request.POST)
        if review_form.is_valid():
            product = Product.objects.get(id=request.POST['product_id'])
            author = request.user
            # Check if there is any review posted by this user on this product
            if singleton_review(author, product):
                data={'message':"You already post a review for this product"}
                print("Already a review")
                return JsonResponse(data)
            
            rating = request.POST['rating']
            comment = request.POST['comment']

            review = Review.objects.create(rating=rating, comment=comment, author=author, product=product)
            review.save()
            # Return all update reviews
            data={'review_id':review.id,
                  'author':review.author.username,
                  'date_created':format_date(review.date_created),
                  'rating':review.rating,
                  'comment':review.comment,}
            print("Valid")
            return JsonResponse(data)
        else:
            print("The form is not valid")
            print(review_form.errors.as_data())
            return HttpResponse("No posted")
            
    else:
        print("An error has ocurred")
        # Handle GET request
        return redirect('Details')
    
def singleton_review(author, product):
    review = Review.objects.filter(author=author, product=product)
    if review:
        return True
    else:
        return False
    
def format_date(date):
    date_string = str(date)
    date = datetime.datetime.fromisoformat(date_string)
    formatted_date = date.strftime('%B %d, %Y, %I:%M %p')

    return formatted_date