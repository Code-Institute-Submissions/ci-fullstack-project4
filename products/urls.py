from django.urls import path
import products.views

urlpatterns = [
    path('', products.views.index,
         name="home_page_route"),
    path('create', products.views.input_product,
         name="create_product_route"),
    path('update/<int:product_id>', products.views.update_product,
         name="update_product_route"),
    path('delete/<int:product_id>', products.views.delete_product,
         name="delete_product_route"),
    path('directory', products.views.directory,
         name="product_directory_route"),
    path('details/<int:product_id>', products.views.detail_view,
         name="product_detail_route"),
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