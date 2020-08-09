from django.urls import path
import products.views

urlpatterns = [
    path('', products.views.index),
    path('create', products.views.input_product,
         name="create_product_route"),
    path('update/<product_id>', products.views.update_product,
         name="update_product_route"),
    path('breakfast', products.views.category_view,
         name="category_product_route"),
    path('biscuits-and-cookies', products.views.category_view,
         name="category_product_route"),
    path('grains-and-dried-beans', products.views.category_view,
         name="category_product_route"),
    path('nuts', products.views.category_view,
         name="category_product_route"),
    path('baking-ingredients', products.views.category_view,
         name="category_product_route"),
    path('fresh-produce', products.views.category_view,
         name="category_product_route")
]