from django.contrib import admin
from .models import FoodItem, Household, StorageLocation, Member
# Register your models here.

admin.site.register(FoodItem)
admin.site.register(StorageLocation)


class MemberInline(admin.TabularInline):
    model = Member


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [MemberInline]
