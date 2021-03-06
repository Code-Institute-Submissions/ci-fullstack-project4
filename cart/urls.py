from django.urls import path
import cart.views

urlpatterns = [
    path('view', cart.views.view_cart,
         name="view_cart"),
    path('add/<product_id>', cart.views.add_to_cart,
         name="add_to_cart"),
    path('subtract/<product_id>', cart.views.subtract_from_cart,
         name="subtract_from_cart"),
    path('update/<product_id>', cart.views.manual_update_qty,
         name="update_cart_qty"),
    path('remove/<product_id>', cart.views.remove_item_from_cart,
         name="remove_from_cart")
]