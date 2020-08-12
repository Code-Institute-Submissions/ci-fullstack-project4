from django.shortcuts import (render, reverse,
                              HttpResponse, get_object_or_404)
from django.conf import settings
import stripe

from products.models import Product
from django.contrib.sites.models import Site
# Create your views here.


def checkout(request):
    # pass API-Key to Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # get the shopping cart
    cart = request.session.get('shopping_cart', {})

    line_items = []
    all_product_ids = []

    for product_id, product in cart.items():
        # retrieve the product's updated information from database
        current_product = get_object_or_404(Product, pk=product_id)
        item = {
            "name": current_product.name,
            # convert to cents and make it int
            "amount": int(current_product.get_current_price()*100),
            "quantity": product.get("qty"),
            "currency": "sgd"
        }
        line_items.append(item)
        all_product_ids.append(str(product_id))

    # get the current website
    current_site = Site.objects.get_current()

    # get the domain name
    domain = current_site.domain

    # create a payment session for this transaction
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],  # only credit cards
        line_items=line_items,
        client_reference_id=request.user.id,
        metadata={
            "all_product_ids": ",".join(all_product_ids)
        },
        mode="payment",
        success_url=domain + reverse("checkout_success"),
        cancel_url=domain + reverse("checkout_cancelled"),
    )
    print(session)
    return render(request, "checkout/checkout.template.html", {
        "session_id": session.id,
        "public_key": settings.STRIPE_PUBLISHABLE_KEY
    })


def checkout_success(request):
    return HttpResponse("checkout success")


def checkout_cancel(request):
    return HttpResponse("checkout cancelled")
