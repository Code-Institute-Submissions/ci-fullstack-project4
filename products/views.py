from django.shortcuts import (render, reverse,
                              redirect, get_object_or_404)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Product, Category, Brand, Subcategory, Usage
from .forms import ProductForm, SearchForm
from django.db.models import Q
import datetime
import re
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


# Create your views here.


class IndexView(TemplateView):
    template_name = "products/index.template.html"
    model = Category

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all products on offer
        context['categories'] = Category.objects.all()
        context['products_on_offer'] = Product.objects.filter(
            status__exact='o')
        return context


class DirectoryView(ListView):
    model = Product
    search_input = ""
    form_class = SearchForm
    template_name = "products/directory.template.html"

    def get_queryset(self):
        # update the existing product found
        return self.model.objects.all()

    def get(self, request, *args, **kwargs):
        self.search_form = self.form_class(self.request.GET)

        # always true query:
        queries = ~Q(pk__in=[])
        # if a name is specified, add it to the query
        if ('search' in self.request.GET and self.request.GET['search']):
            self.search_input = self.request.GET['search']
            queries = queries & Q(name__icontains=self.search_input)

        # if a min_price is specified, add it to query
        if 'min_price' in self.request.GET and self.request.GET['min_price']:
            min_price = float(self.request.GET['min_price'])
        else:
            min_price = 0.00

        # if a max_price is specified, add it to query
        if 'max_price' in self.request.GET and self.request.GET['max_price']:
            max_price = float(self.request.GET['max_price'])
        else:
            max_price = 99999.99

        queries = queries & Q(root_price__gte=min_price) & Q(
            root_price__lte=max_price)

        self.object_list = self.model.objects.filter(queries)

        context = self.get_context_data(products=self.object_list,
                                        search_form=self.search_form,
                                        search_input=self.search_input)

        return self.render_to_response(context)


class CategoryView(ListView):
    model = Product
    template_name = 'products/bycategory.template.html'

    def get_queryset(self):
        path = self.request.get_full_path()
        result = re.search(r"(?!.*/).+", path).group(0)
        result_list = result.split("-")
        regex_str = result_list[0]
        self.page_title = " ".join(result_list)
        return self.model.objects.filter(
            category__name__icontains=regex_str).order_by('name')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(searched_products=self.object_list,
                                        page_title=self.page_title
                                        )
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/details.template.html'


class BrandListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('products.view_brand')
    model = Brand
    template_name = 'products/brands.template.html'
    ordering = ['name']


class BrandCreate(LoginRequiredMixin, PermissionRequiredMixin, 
                  SuccessMessageMixin, CreateView):
    permission_required = ('products.add_brand')
    model = Brand
    fields = ['name']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home_page_route')
    success_message = "Brand %(name)s was created successfully"


class BrandUpdate(LoginRequiredMixin, PermissionRequiredMixin,
                  SuccessMessageMixin, UpdateView):
    permission_required = ('products.change_brand')
    model = Brand
    fields = ['name']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('home_page_route')
    success_message = "Brand %(name)s was updated successfully"


class BrandDelete(LoginRequiredMixin, PermissionRequiredMixin,
                  SuccessMessageMixin, DeleteView):
    permission_required = ('products.delete_brand')
    model = Brand
    fields = ['name']
    success_url = reverse_lazy('home_page_route')
    success_message = "Brand %(name)s was deleted successfully"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(BrandDelete, self).delete(request, *args, **kwargs)


@login_required
@permission_required('products.add_product')
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
@permission_required('products.change_product')
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


@login_required
@permission_required('products.delete_product')
def delete_product(request, product_id):
    product_to_delete = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product_to_delete.delete()
        messages.success(
                request,
                f"{product_to_delete}, id={product_id}"
                f" has been deleted from the system, on"
                f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
        return redirect(reverse(index))
