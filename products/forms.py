from django import forms
from .models import Product, Category

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from crispy_forms.bootstrap import InlineField, FormActions, Div
from crispy_forms.layout import Layout, Submit, ButtonHolder

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

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    fieldsets = (
        (None, {
            'fields': ('search')
        }),
        ('Advanced options', {
            'fields': ('min_price', 'max_price'),
        }),
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.method = "GET"
        self.helper.layout = Layout(
            Div(
                Div('search', css_class="col-sm-3"),
                Div('min_price', css_class="col-sm-3"),
                Div('max_price', css_class="col-sm-3")
            )
        )
