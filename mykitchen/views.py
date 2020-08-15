from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import HouseholdForm, MemberFormSet
from .models import Member, Household
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.


@login_required
def index(request):
    # get user = request.user,
    # get household id from Parameter
    user = request.user

    # check if logged in user is household member
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None

    # if owner logs in, check if household exists
    try:
        household = Household.objects.get(owner=user)
    except Household.DoesNotExist:
        household = None

    #if member exists, get household
    if member:
        household = member.household
    
    if household is None:
        household = ""
        messages.success(
                request,
                "Please register the household and link the members."
        )
    return render(request, 'mykitchen/mykitchen_index.template.html', {
        'household': household
    })


def register_household(request):
    if request.method == 'POST':
        house_form = HouseholdForm(request.POST)
        member_form = MemberFormSet(request.POST)
        # if the form is validated
        if house_form.is_valid():
            household = house_form.save()
            if member_form.isvalid():
                members = member_form.save()
                messages.success(
                        request,
                        f"Your Household {household.name} profile"
                        f" has been created on"
                        f" {datetime.datetime.today().strftime('%b %d, %Y, %H:%M:%S')}")
                return redirect(reverse(index))
    house_form = HouseholdForm()
    member_form = MemberFormSet()
    return render(request, 'mykitchen/register_household.template.html', {
        'house_form': house_form,
        'member_form': member_form
    })
