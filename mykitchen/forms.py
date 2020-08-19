from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from .models import Household, Member, StorageLocation, FoodItem
from django.db.models import Q


class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ('name',)
        widgets = {
            'owner': forms.HiddenInput()
        }


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'member-form'
        self.helper.form_class = 'form-inline'
        self.helper.method = "POST"
        self.helper.layout = Layout(
            Div(
                Div('user', css_class="col-sm-3")
            )
        )
        members = Member.objects.all()
        self.fields['user'].queryset = self.fields['user'].queryset.exclude(
            Q(user__in=members))

    class Meta:
        model = Member
        fields = ('user',)


MemberFormSet = inlineformset_factory(
    Household, Member, form=MemberForm, fields=('user',),
    extra=3, fk_name="household", can_delete=True)


class StorageLocationForm(forms.ModelForm):
    class Meta:
        model = StorageLocation
        fields = ('name', 'storage_temperature', 'storage_type',)
        exclude = ('edited_by', 'household')


class FoodItemForm(forms.ModelForm):
    expiry_date = forms.DateField(widget=forms.DateInput(
        format=('%m/%d/%Y'), attrs={'class': 'datepicker'}
        ))

    class Meta:
        model = FoodItem
        fields = ('food', 'quantity', 'remarks', 'threshold',
                  'package', 'expiry_date')
        widgets = {
        }
        exclude = ('edited_by',)

