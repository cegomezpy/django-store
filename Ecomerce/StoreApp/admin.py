from django.contrib import admin
from .models import Category, Product, ProductImage, Events, EventsImages

# Register your models here.

class ImageInlineProducts(admin.TabularInline):
    model = ProductImage
    extra = 1

class ImageInlineEvents(admin.TabularInline):
    model = EventsImages
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'discount_price', 'in_stock', 'available')
    inlines = [ImageInlineProducts]

class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'discount_price', 'available')
    inlines = [ImageInlineEvents]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Events, EventsAdmin)