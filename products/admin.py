from django.contrib import admin
from .models import Brand, Category, Country, Subcategory, Usage

# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Subcategory)
admin.site.register(Usage)
