from django.urls import path
import mykitchen.views

urlpatterns = [
    path('', mykitchen.views.index,
         name="mykitchen_home_page"),
    path('register', mykitchen.views.register_household,
         name="mykitchen_register")
]