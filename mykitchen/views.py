from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import HouseholdForm, MemberFormSet
from .models import Member, Household
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
import datetime

# Create your views here.


@login_required
def index(request):
    # get user = request.user,
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

    # if member exists, get household
    if member:
        household = member.household

    if household is None:
        household = ""
        messages.info(
                request,
                "Please register the household and link the members."
        )
    return render(request, 'mykitchen/mykitchen_index.template.html', {
        'household': household
    })


def view_household(request):
    return render(request, 'mykitchen/view_household.template.html', {
    })


def register_household(request):
    if request.method == 'POST':
        house_form = HouseholdForm(request.POST)
        member_form = MemberFormSet(request.POST)

        # if the form is validated
        if house_form.is_valid():
            household = house_form.save(commit=False)
            household.owner = request.user
            owner_group = Group.objects.get(name='owner_group')
            owner_group.user_set.add(household.owner)
            if member_form.is_valid():
                household.save()
                members = member_form.save(commit=False)
                for member in members:
                    member_group = Group.objects.get(name='member_group')
                    try:
                        user = User.objects.get(username=member)
                    except User.DoesNotExist:
                        user = None
                    member_group.user_set.add(user)
                    member.household = household
                    member.save()
                messages.success(
                    request,
                    f"Your household profile {household.name}"
                    f" has been created on"
                    f" {datetime.datetime.today().strftime('%b %d, %Y, %H:%M:%S')}")
                return redirect(reverse(index))
    house_form = HouseholdForm()
    member_form = MemberFormSet()
    return render(request, 'mykitchen/register_household.template.html', {
        'house_form': house_form,
        'member_form': member_form
    })
