from django.shortcuts import render
from .models import Product, Events
from django.db.models import Q, Avg, Count
from .forms import PriceForm, CategoryForm, SearchForm, CategoryEventsForm

# Create your views here.
# Get store view
def store(request, header, form_price=None, form_category=None, search_form=None, query=None):
    condition = header == "products"
    print(condition)
    print(query)
    # If query is None, return a new template
    if query is None:
        # Get all query
        form_price = PriceForm()
        form_category = CategoryForm(data=request.GET) if condition else CategoryEventsForm()
        search_form = SearchForm()
        query = Product.objects.all() if condition else Events.objects.all()
        #query = annotate_rating(query)
    if header == "search":
        for i in query:
            for j in i:
                j.condition = isinstance(j, Product)
                print(j, "condition", j.condition)
        context = {"header":header, "search_form":search_form}
    else:
        context = {"header":header, "form_price": form_price, "form_category": form_category, 'search_form':search_form}
    if query: context.update({"query":query})
    return render(request, 'store.html', context)

# Get query filtered
def filter(request, header):
    condition = header == "products"
    print(condition)
    if request.GET:
        # Get query
        query = Product.objects.all() if condition else Events.objects.all()
        # Get data from forms
        form_price = PriceForm(data=request.GET)
        form_category = CategoryForm(data=request.GET) if condition else CategoryEventsForm(data=request.GET)
        search_form = SearchForm(data=request.GET)
        # Filter query
        query, form_price = filter_price(query, form_price)
        query, form_category = filter_category(query, form_category)

        return store(request, header, form_price=form_price, form_category=form_category, search_form=search_form, query=query)

# Manage price forme
def filter_price(query, form_price):
    if form_price.is_valid():
        # If min price was entered filter by min price
        if form_price.cleaned_data["min_price"]:
            min = form_price.cleaned_data["min_price"]
            # Filter by discount or original price
            query = query.filter(
                Q(price__gte=min) | Q(discount_price__gte=min))
        # If max price was entered filter by max price
        if form_price.cleaned_data["max_price"]:
            max = form_price.cleaned_data["max_price"]
            # Filter by discount or original price
            query = query.filter(
                Q(price__lte=max) | Q(discount_price__lte=max))
            
    return query, form_price

# Manage category form
def filter_category(query, form_category):
    if form_category.is_valid():
        # Filter by union
        categories = "categories"
        if form_category.cleaned_data[categories].exists():
            category_set = form_category.cleaned_data[categories]
            query = query.filter(
                categories__in=category_set).distinct()
    return query, form_category

def search(request, search_form=None):
    print("Empieza a buscar")
    query = [Product.objects.all(), Events.objects.all()]
    filtered = []
    header = "search"
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        if search_form.cleaned_data['search_bar']:
            for i in query:
                filter = i.filter(name__icontains=search_form.cleaned_data['search_bar'])
                if filter.exists(): filtered.append(filter)
    print("Filtered", filtered)
    return store(request, header, query=filtered, search_form=search_form)

def annotate_rating(query):
    new_products = query.annotate(rating=Avg('review__rating'), review_length=Count('review'))
    return new_products