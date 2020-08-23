from django import forms
from .models import Product

from crispy_forms.helper import FormHelper
from crispy_forms import layout
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import Div


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'brand', 'desc', 'origin', 'weight_per_pack',
                  'qty_per_pack', 'barcode_spec', 'barcode_no', 'image',
                  'root_price', 'multiplier', 'category', 'subcategory',
                  'usage', 'status')
        widgets = {
            'editor': forms.HiddenInput(),
            'date_edited': forms.HiddenInput()
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    min_price = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, help_text="e.g. 0.30")
    max_price = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, help_text="e.g. 9.99")

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.method = "GET"
        self.helper.layout = layout.Layout(
            Div('search', css_class="col align-self-center"),
            Div('min_price', css_class="col"),
            Div('max_price', css_class="col"),
            Submit('submit', 'Search', css_class="btn-success align-self-center")
        )

