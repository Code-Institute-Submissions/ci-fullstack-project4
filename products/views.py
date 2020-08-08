from django.shortcuts import render, HttpResponse
from .models import Product, Category

# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/index.template.html', {
        'products': products,
        'categories': categories
    })

def breakfast(request):
    """View function for Breakfast Products only"""

    breakfast_products = Product.objects.filter(
        category__name__iexact='breakfast').order_by('name')
    return render(request, 'products/breakfast.template.html', {
        'breakfast_products': breakfast_products
    })