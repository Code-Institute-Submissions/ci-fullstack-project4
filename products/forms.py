from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'brand', 'desc', 'origin', 'weight_per_pack',
                  'qty_per_pack', 'barcode_spec', 'barcode_no', 'image',
                  'root_price', 'category', 'subcategory', 'usage')
        widgets = {
            'editor': forms.HiddenInput(),
            'date_edited': forms.HiddenInput()
        }