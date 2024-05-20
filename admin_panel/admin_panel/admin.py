from django.contrib import admin
from .models import Product, Subcategory, Category, Basket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'description', 'price', 'amount', 'image', 'image_tag', 'subcategory', 'created', 'updated']
    readonly_fields = ['image_tag', 'created', 'updated']
    search_fields = ['title__startswith']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'title', 'category','created', 'updated')
    readonly_fields = ['created', 'updated']
    search_fields = ['title__startswith']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'title','created', 'updated')
    readonly_fields = ['created', 'updated']
    search_fields = ['title__startswith']


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id', 'products']

    def	_products(self, row):
        return ', '.join([x.title for x in row.products.all()])
    _products.short_description = 'products'
