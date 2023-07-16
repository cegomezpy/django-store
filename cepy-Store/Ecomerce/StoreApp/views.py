from django.shortcuts import render
from .models import Product
from django.db.models import Q, Avg, Count
from .forms import PriceForm, CategoryForm, SearchForm

# Create your views here.
# Get store view
def store(request, products=None, form_price=None, form_category=None, search_form=None):
    # If products is None, return a new template
    if products is None:
        # Instanciate forms
        form_price = PriceForm()
        form_category = CategoryForm()
        search_form = SearchForm()
        # Get all products
        products = Product.objects.all()
        products = annotate_rating(products)
        context = {"products": products, "form_price": form_price,
                   "form_category": form_category, 'search_form':search_form,'rating_stars':[1, 2, 3, 4, 5]}
    else:
        # If products in the queryset products
        if products.exists():
            products = annotate_rating(products)
            context = {"products": products, "form_price": form_price,
                       "form_category": form_category, 'search_form':search_form, 'rating_stars':[1, 2, 3, 4, 5]}
        # If none products in the queryset, no results for the selected filter
        else:
            # products not passed to context, template will show a message
            context = {"form_price": form_price,
                       "form_category": form_category,
                       'search_form':search_form}
    return render(request, 'store.html', context)

# Get products filtered
def filter(request):
    if request.GET:
        # Get products
        products = Product.objects.all()
        # Get data from forms
        form_price = PriceForm(data=request.GET)
        form_category = CategoryForm(data=request.GET)
        search_form = SearchForm(data=request.GET)
        # Manage price form
        if form_price.is_valid():
            print("Form price is valid")
            # If min price was entered filter by min price
            if form_price.cleaned_data["min_price"]:
                min = form_price.cleaned_data["min_price"]
                # Filter by discount or original price
                products = products.filter(
                    Q(price__gte=min) | Q(discount_price__gte=min))
            # If max price was entered filter by max price
            if form_price.cleaned_data["max_price"]:
                max = form_price.cleaned_data["max_price"]
                # Filter by discount or original price
                products = products.filter(
                    Q(price__lte=max) | Q(discount_price__lte=max))
        # Manage category form
        if form_category.is_valid():
            # Filter by union
            if form_category.cleaned_data["categorys"].exists():
                print(form_category.cleaned_data)
                category_set = form_category.cleaned_data["categorys"]
                products = products.filter(
                    categories__in=category_set).distinct()
                
        if search_form.is_valid():
            if search_form.cleaned_data['search_bar']:
                products = products.filter(name__icontains=search_form.cleaned_data['search_bar'])   
        
        return store(request, products=products, form_category=form_category, form_price=form_price, search_form=search_form)
    
def annotate_rating(products):
    new_products = products.annotate(rating=Avg('review__rating'), review_length=Count('review'))
    return new_products