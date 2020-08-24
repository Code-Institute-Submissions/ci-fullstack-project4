from django.shortcuts import (render, reverse,
                              redirect, get_object_or_404)
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
    """Home Page View"""
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
    """Directory Page View"""
    model = Product
    search_input = ""
    form_class = SearchForm
    template_name = "products/directory.template.html"

    def get_queryset(self):
        # default : find all products
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
    """ View Products By Category """
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
    """ View Product Details """
    model = Product
    template_name = 'products/details.template.html'


class BrandListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ View All Brands (Staff Access) """
    permission_required = ('products.view_brand')
    model = Brand
    template_name = 'products/brands.template.html'
    ordering = ['name']


class BrandCreate(LoginRequiredMixin, PermissionRequiredMixin,
                  SuccessMessageMixin, CreateView):
    """ Input Brands (Staff Access) """
    permission_required = ('products.add_brand')
    model = Brand
    fields = ['name']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home_page_route')
    success_message = "Brand %(name)s was created successfully"


class BrandUpdate(LoginRequiredMixin, PermissionRequiredMixin,
                  SuccessMessageMixin, UpdateView):
    """ Update Brands (Staff Access) """
    permission_required = ('products.change_brand')
    model = Brand
    fields = ['name']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('home_page_route')
    success_message = "Brand %(name)s was updated successfully"


class BrandDelete(LoginRequiredMixin, PermissionRequiredMixin,
                  SuccessMessageMixin, DeleteView):
    """ Delete Brands (Staff Access) """
    permission_required = ('products.delete_brand')
    model = Brand
    fields = ['name']
    success_url = reverse_lazy('home_page_route')
    success_message = "Brand %(name)s was deleted successfully"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(BrandDelete, self).delete(request, *args, **kwargs)


class CreateProduct(LoginRequiredMixin, PermissionRequiredMixin,
                    SuccessMessageMixin, CreateView):
    """ Input Product (Staff Access) """
    permission_required = ('products.add_product')
    model = Product
    form_class = ProductForm
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('home_page_route')
    success_message = "Product %(name)s was created successfully on %(date)s"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        new_product = form.save(commit=False)
        new_product.editor = self.request.user
        new_product.date_edited = datetime.datetime.now()
        self.object = new_product.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % {
            'name': self.object.name,
            'date': self.object.date_edited.strftime('%b %d, %Y, %H:%M:%S')
        }


class UpdateProduct(LoginRequiredMixin, PermissionRequiredMixin,
                    SuccessMessageMixin, UpdateView):
    """ Update Product (Staff Access) """
    permission_required = ('products.change_product')
    model = Product
    form_class = ProductForm
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('home_page_route')
    success_message = "Product %(name)s was updated successfully on %(date)s"

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        edited_product = form.save(commit=False)
        edited_product.editor = self.request.user
        edited_product.date_edited = datetime.datetime.now()
        self.object = edited_product.save()
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % {
            'name': self.object.name,
            'date': self.object.date_edited.strftime('%b %d, %Y, %H:%M:%S')
        }


class DeleteProduct(LoginRequiredMixin, PermissionRequiredMixin,
                    SuccessMessageMixin, DeleteView):
    """ Delete Product (Staff Access) """
    permission_required = ('products.delete_product')
    model = Product
    success_url = reverse_lazy('home_page_route')
    success_message = "Product %(name)s was deleted successfully."

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteProduct, self).delete(request, *args, **kwargs)
