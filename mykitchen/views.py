from django.shortcuts import render
from django.contrib import messages
from .forms import HouseholdForm, MemberFormSet
# Create your views here.


def index(request):
    # get user = request.user,
    # get household id from Parameter

    messages.success(
                request,
                "Test messages"
    )
    return render(request, 'mykitchen/mykitchen_index.template.html', {
    })


def register_household(request):
    if request.method == 'POST':
        house_form = HouseholdForm(request.POST)
         # if the form is validated
        if house_form.is_valid():
            household = house_form.save(commit=False)

    house_form = HouseholdForm()
    member_form = MemberFormSet()
    return render(request, 'mykitchen/register_household.template.html', {
        'house_form': house_form,
        'member_form': member_form
    })