

def cart_contents(request):
    cart = request.session.get("shopping_cart",{})
    return {
        'shopping_cart': cart,
        'item_count':len(cart)
}
