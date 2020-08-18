from django.urls import path
import mykitchen.views

urlpatterns = [
    path('', mykitchen.views.index,
         name="mykitchen_home_page"),
    path('register', mykitchen.views.register_household,
         name="register_household"),
    path('view-household/<household_id>', mykitchen.views.view_household,
         name="view_household"),
    path('edit-household/<household_id>', mykitchen.views.edit_household,
         name="edit_household"),
    path('delete-household/<household_id>', mykitchen.views.delete_household,
         name="delete_household"),
    path('view-storage/<household_id>', mykitchen.views.view_storage_location,
         name="view_storage_location"),
    path('add-storage/<household_id>', mykitchen.views.add_storage_location,
         name="add_storage_location")
]
