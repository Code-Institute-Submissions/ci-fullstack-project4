from django.contrib import admin
from .models import Brand, Category, Country, Product, Subcategory, Usage

# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Product)
admin.site.register(Subcategory)
admin.site.register(Usage)
