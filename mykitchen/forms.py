from django import forms
from django.forms.models import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from .models import Household, Member


class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ('name',)
        widgets = {
            'owner': forms.HiddenInput()
        }


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'member-form'
        self.helper.form_class = 'form-inline'
        self.helper.method = "POST"
        self.helper.layout = Layout(
            Div(
                Div('user', css_class="col-sm-3")
            )
        )
        super(MemberForm, self).__init__(*args, **kwargs)

        class Meta:
            model = Member


MemberFormSet = inlineformset_factory(
    Household, Member, form=MemberForm, fields=('user',),
    extra=3, fk_name="household", can_delete=True)
