from django.shortcuts import (render, redirect, reverse,
                              get_object_or_404)
from django.contrib import messages
from products.models import Product

# Create your views here.


def add_to_cart(request, product_id):
    cart = request.session.get('shopping_cart', {})
    print(cart)
    if product_id not in cart:
        product = get_object_or_404(Product, pk=product_id)
        cart[product_id] = {
            'id': product_id,
            'name': product.name,
            'unit_cost': product.get_current_price(),
            'qty': 1
        }
        """save the cart into the shopping cart session"""
        request.session['shopping_cart'] = cart
        messages.success(request, f'{product.name} been added to your cart!')
        return redirect(reverse('products.views.index'))
    else:
        cart[product_id]['qty'] += 1
        """save the cart into the shopping cart session again"""
        request.session['shopping_cart'] = cart
        return redirect(reverse('products.views.index'))


