from django.shortcuts import (render, reverse,
                              redirect, get_object_or_404)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm
import datetime
import re

# Create your views here.


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/index.template.html', {
        'products': products,
        'categories': categories
    })


def category_view(request):
    """View function for view by categorical Products """
    path = request.get_full_path()
    result = re.search(r"(?!.*/).+", path).group(0)
    result_list = result.split("-")
    regex_str = result_list[0]
    page_title = " ".join(result_list)
    searched_products = Product.objects.filter(
        category__name__icontains=regex_str).order_by('name')
    return render(request, 'products/bycategory.template.html', {
        'searched_products': searched_products,
        'page_title': page_title
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
            messages.success(
                request,
                f"New Product {input_form.data['name']}"
                f" has been entered into the system on"
                f" {new_product.date_edited.strftime('%b %d, %Y, %H:%M:%S')}")
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


@login_required
@permission_required('products.update_product')
def update_product(request, product_id):
    product_to_update = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        update_form = ProductForm(request.POST, instance=product_to_update)
        if update_form.is_valid():
            edited_product = update_form.save(commit=False)
            edited_product.editor = request.user
            edited_product.date_edited = datetime.datetime.now()
            edited_product.save()
            messages.success(
                request,
                f"Product {update_form.data['name']}"
                f" has been updated in the system, on"
                f" {edited_product.date_edited.strftime('%b %d, %Y, %H:%M:%S')}")
            return redirect(reverse(index))
        else:
            return render(request, 'products/update_product.template.html', {
                      'form': update_form
                      })
    else:
        update_form = ProductForm(instance=product_to_update)
        return render(request, 'products/update_product.template.html', {
                      'form': update_form
                      })
