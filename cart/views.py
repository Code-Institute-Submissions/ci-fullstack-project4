from django.shortcuts import (render, redirect, reverse,
                              get_object_or_404)
from django.contrib import messages
from products.models import Product
import products.views
import datetime
from urllib.parse import urlparse 

# Create your views here.


def add_to_cart(request, product_id):
    cart = request.session.get('shopping_cart', {})
    if product_id not in cart:
        product = get_object_or_404(Product, pk=product_id)
        cart[product_id] = {
            'id': product_id,
            'name': product.name,
            'image': product.image,
            'unit_cost': round(float(product.get_current_price()), 2),
            'qty': 1,
            'datetime_added': datetime.datetime.now().strftime(
                              '%b %d, %Y, %H:%M:%S')
        }
        """save the cart into the shopping cart session"""
        request.session['shopping_cart'] = cart
        messages.success(request, f'{product.name} been added to your cart!')
        return redirect(reverse(products.views.index))
    else:
        cart[product_id]['qty'] += 1
        """save the cart into the shopping cart session again"""
        request.session['shopping_cart'] = cart
        current_path = urlparse(request.META['HTTP_REFERER']).path
        if current_path == '/cart/view':
            return redirect(reverse(view_cart))
        else:
            messages.success(request, f'{product.name} been added'
                             f'to your cart!')
            return redirect(reverse(products.views.index))


def view_cart(request):
    cart = request.session.get('shopping_cart', {})
    print(cart)
    print(len(cart))
    #del request.session['shopping_cart']
    return render(request, 'cart/view_cart.template.html', {
        'cart': cart
    })
