from .StoreApp.models import Category
from .StoreApp.forms import SearchForm

def categorys_list(request):
    categorys = Category.objects.all()

    return {"categories": categorys}

def search_form(request):
    search_form = SearchForm()
    return {'search_form':search_form}