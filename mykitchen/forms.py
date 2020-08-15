from django import forms
from django.forms.models import inlineformset_factory

from .models import Household, Member


class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ('name',)
        widgets = {
            'owner': forms.HiddenInput()
        }


MemberFormSet = inlineformset_factory(
    Household, Member, fields=('user',), can_delete=True)
