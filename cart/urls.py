from django.urls import path
import cart.views

urlpatterns = [
    path('view', cart.views.view_cart,
         name="view_cart"),
    path('add/<product_id>', cart.views.add_to_cart,
         name="add_to_cart"),
    path('subtract/<product_id>', cart.views.subtract_from_cart,
         name="subtract_from_cart")
]