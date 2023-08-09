from .StoreApp.models import Category, Product, Events
from .StoreApp.forms import SearchForm

def categorys_list(request):
    products = Product.objects.all()
    events = Events.objects.all()
    categories_products = Category.objects.all().filter(products__in=products).distinct()
    print(categories_products)
    categories_events = Category.objects.all().filter(events__in=events).distinct()

    return {"categories_products":categories_products, "categories_events":categories_events}

def search_form(request):
    search_form = SearchForm()
    return {'search_form':search_form}

def rating_stars(request):
    return {'rating_stars':[1, 2, 3, 4, 5]}