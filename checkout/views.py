from django.shortcuts import (render, reverse,
                              HttpResponse, get_object_or_404)
from django.conf import settings
import stripe

from products.models import Product
from .models import Purchase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
import datetime
import random
# Create your views here.

endpoint_secret = settings.STRIPE_ENDPOINT_SECRET


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
    return render(request, "checkout/checkout.template.html", {
        "session_id": session.id,
        "public_key": settings.STRIPE_PUBLISHABLE_KEY
    })


def checkout_success(request):
    # clear the shopping cart after checkout success
    request.session['shopping_cart'] = {}
    prefix = datetime.datetime.now().strftime('%m%d%Y')
    invoice_num = prefix+str(random.randrange(10000000, 100000000))
    return render(request, "checkout/checkout_success.template.html", {
        'invoice_num': invoice_num
    })


def checkout_cancel(request):
    return HttpResponse("checkout cancelled")


@csrf_exempt
def payment_completed(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(e)
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        handle_payment(session)

    return HttpResponse(status=200)


def handle_payment(session):

    # get user from User model
    user = get_object_or_404(User, pk=session['client_reference_id'])

    # change the metadata from string back to array
    all_product_ids = session['metadata']['all_product_ids'].split(",")

    for product_id in all_product_ids:
        product = get_object_or_404(Product, pk=product_id)

        purchase = Purchase()
        purchase.product_id = product
        purchase.user_id = user
        purchase.save()
