from django.shortcuts import (render, redirect, reverse,
                              get_object_or_404)
from django.contrib import messages
from products.models import Product
import products.views
import datetime
import re
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
        """ get current path from django request"""
        current_path = urlparse(request.META['HTTP_REFERER']).path
        """ get directory of current path"""
        path_dir = re.search(r"[^/](\w+)", current_path).group(0)
        if path_dir == 'cart':
            return redirect(reverse(view_cart))
        else:
            messages.success(request, f'{cart[product_id].get("name")} been added'
                             f' to your cart!')
            return redirect(reverse(products.views.index))


def view_cart(request):
    cart = request.session.get('shopping_cart', {})
    grand_total = 0
    for k, v in cart.items():
        grand_total += float(v['unit_cost'] * v['qty'])
    # del request.session['shopping_cart']
    return render(request, 'cart/view_cart.template.html', {
        'cart': cart,
        'grand_total': grand_total
    })


def subtract_from_cart(request, product_id):
    cart = request.session.get('shopping_cart', {})
    if product_id in cart and cart[product_id]['qty'] > 1:
        cart[product_id]['qty'] -= 1
    else:
        del cart[product_id]
    """ recalculate grand total """
    grand_total = 0
    for k, v in cart.items():
        grand_total += float(v['unit_cost'] * v['qty'])
    """save the cart into the shopping cart session again"""
    request.session['shopping_cart'] = cart
    return render(request, 'cart/view_cart.template.html', {
        'cart': cart,
        'grand_total': grand_total
    })


def remove_item_from_cart(request, product_id):
    cart = request.session.get('shopping_cart', {})
    if product_id in cart:
        del cart[product_id]
    """ recalculate grand total """
    grand_total = 0
    for k, v in cart.items():
        grand_total += float(v['unit_cost'] * v['qty'])
    """save the cart into the shopping cart session again"""
    request.session['shopping_cart'] = cart
    return render(request, 'cart/view_cart.template.html', {
        'cart': cart,
        'grand_total': grand_total
    })


def manual_update_qty(request, product_id):
    cart = request.session["shopping_cart"]
    if product_id in cart and request.method == "POST":
        """update cart qty"""
        cart[product_id]['qty'] = int(request.POST['qty'])
        """ recalculate grand total """
        grand_total = 0
        for k, v in cart.items():
            grand_total += float(v['unit_cost'] * v['qty'])
        """save back the cart into the session"""
        request.session['shopping_cart'] = cart
    return render(request, 'cart/view_cart.template.html', {
        'cart': cart,
        'grand_total': grand_total
    })
