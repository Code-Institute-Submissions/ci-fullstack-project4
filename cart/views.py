from django.shortcuts import (render, redirect, reverse,
                              get_object_or_404)
from django.contrib import messages
from products.models import Product
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
            'subtotal': round(float(product.get_current_price()), 2),
            'datetime_added': datetime.datetime.now().strftime(
                '%b %d, %Y, %H:%M:%S')
        }
        """save the cart into the shopping cart session"""
        request.session['shopping_cart'] = cart
        messages.success(request, f'{product.name} been added to your cart!')
        return redirect(reverse('home_page_route'))
    else:
        """add the quantity to cart"""
        cart[product_id]['qty'] += 1
        """ recalculate subtotal"""
        cart[product_id]['subtotal'] = int(
            cart[product_id]['qty']) * float(cart[product_id]['unit_cost'])
        """save the cart into the shopping cart session again"""
        request.session['shopping_cart'] = cart
        """ get current path from django request"""
        current_path = urlparse(request.META['HTTP_REFERER']).path
        """ get directory of current path"""
        path_dir = re.search(r"[^/](\w+)", current_path).group(0)
        if path_dir == 'cart':
            return redirect(reverse(view_cart))
        else:
            messages.success(request,
                             f'{cart[product_id].get("name")} has been'
                             f' added to your cart!')
            return redirect(reverse('home_page_route'))


def view_cart(request):
    cart = request.session.get('shopping_cart', {})
    grand_total = 0
    for k, v in cart.items():
        grand_total += float(v['unit_cost'] * v['qty'])
    # if cart is empty,
    if not cart.items():
        return render(request, 'cart/view_empty.template.html')
    else:
        return render(request, 'cart/view_cart.template.html', {
            'cart': cart,
            'grand_total': grand_total
        })


def subtract_from_cart(request, product_id):
    cart = request.session.get('shopping_cart', {})
    if product_id in cart and cart[product_id]['qty'] > 1:
        cart[product_id]['qty'] -= 1
        """ recalculate subtotal"""
        cart[product_id]['subtotal'] = int(
            cart[product_id]['qty']) * float(cart[product_id]['unit_cost'])
    else:
        del cart[product_id]
    """ recalculate grand total """
    grand_total = 0
    for k, v in cart.items():
        grand_total += float(v['unit_cost'] * v['qty'])
    """save the cart into the shopping cart session again"""
    request.session['shopping_cart'] = cart
    if not cart.items():
        return render(request, 'cart/view_empty.template.html')
    else:
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
    if not cart.items():
        return render(request, 'cart/view_empty.template.html')
    else:
        return render(request, 'cart/view_cart.template.html', {
            'cart': cart,
            'grand_total': grand_total
        })


def manual_update_qty(request, product_id):
    cart = request.session["shopping_cart"]
    if product_id in cart and request.method == "POST":
        """update cart qty"""
        cart[product_id]['qty'] = int(request.POST['qty'])
        """update cart subtotal"""
        cart[product_id]['subtotal'] = int(
            request.POST['qty']) * float(cart[product_id]['unit_cost'])
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
