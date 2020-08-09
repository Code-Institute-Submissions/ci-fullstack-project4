from django.urls import path
import products.views

urlpatterns = [
    path('', products.views.index),
    path('breakfast', products.views.breakfast,
         name="view_breakfast_product"),
    path('create', products.views.input_product,
         name="create_product_route")
]