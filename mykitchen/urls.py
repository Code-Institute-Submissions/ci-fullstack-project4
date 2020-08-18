from django.urls import path
import mykitchen.views

urlpatterns = [
    path('', mykitchen.views.index,
         name="mykitchen_home_page"),
    path('register', mykitchen.views.register_household,
         name="register_household"),
    path('view-household/<int:household_id>', mykitchen.views.view_household,
         name="view_household"),
    path('edit-household/<int:household_id>', mykitchen.views.edit_household,
         name="edit_household"),
    path('delete-household/<int:household_id>',
         mykitchen.views.delete_household,
         name="delete_household"),
    path('view-storage/<int:household_id>',
         mykitchen.views.view_storage_location,
         name="view_storage_location"),
    path('add-storage/<int:household_id>',
         mykitchen.views.add_storage_location,
         name="add_storage_location"),
    path('update-storage/<int:household_id>/<int:storage_id>',
         mykitchen.views.update_storage_location,
         name="update_storage_location"),
    path('delete-storage/<int:household_id>/<int:storage_id>',
         mykitchen.views.delete_storage_location,
         name="delete_storage_location")
]
