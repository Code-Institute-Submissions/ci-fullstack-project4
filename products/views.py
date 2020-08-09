from django.shortcuts import render, HttpResponse, reverse, redirect
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, permission_required
import datetime

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


@login_required
@permission_required('products.input_product')
def input_product(request):
    if request.method == 'POST':
        input_form = ProductForm(request.POST)

        # if the form is validated
        if input_form.is_valid():
            new_product = input_form.save(commit=False)
            new_product.editor = request.user
            new_product.date_edited = datetime.datetime.now()
            new_product.save()
            return redirect(reverse(index))
        else:
            return render(request, 'products/input_product.template.html', {
                          'form': input_form
                          })
    else:
        input_form = ProductForm()
        return render(request, 'products/input_product.template.html', {
            'form': input_form
        })