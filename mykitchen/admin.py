from django.contrib import admin
from .models import Household,Location,FoodItem
# Register your models here.

admin.site.register(FoodItem)
admin.site.register(Household)
admin.site.register(Location)