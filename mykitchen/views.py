from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import HouseholdForm, MemberFormSet
from .models import Member, Household
from django.contrib.auth.decorators import login_required, permission_required
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


@login_required
@permission_required(['mykitchen.view_household',
                      'mykitchen.view_member'])
def view_household(request, household_id):
    # if request.user = owner
    household = Household.objects.get(id=household_id)
    members = Member.objects.filter(household=household)
    return render(request, 'mykitchen/view_household.template.html', {
        'household': household,
        'members': members
    })


@login_required
@permission_required(['mykitchen.add_household',
                      'mykitchen.add_member'])
def register_household(request):
    if request.method == 'POST':
        house_form = HouseholdForm(request.POST)
        member_formset = MemberFormSet(request.POST, prefix="member")
        # if the form is validated
        if house_form.is_valid():
            house_form_instance = house_form.save(commit=False)
            house_form_instance.owner = request.user
            owner_group = Group.objects.get(name='owner_group')
            owner_group.user_set.add(house_form_instance.owner)
            if member_formset.is_valid():
                members_form_instance = member_formset.save(commit=False)
                house_form_instance.save()
                for form_instance in members_form_instance:
                    member_group = Group.objects.get(name='member_group')
                    try:
                        user = User.objects.get(username=form_instance)
                    except User.DoesNotExist:
                        user = None
                    # check if user belongs to another household
                    try:
                        member = Member.objects.get(user=user)
                    except Member.DoesNotExist:
                        member = None

                    if member is not None or user is None:
                        messages.error(request,
                                       f"{user}already belongs to another"
                                       " household or No such User.")
                        return redirect(reverse(index))
                    else:
                        # assign user to group
                        member_group.user_set.add(user)
                        # save form data
                        form_instance.household = house_form_instance
                        form_instance.save()
                messages.success(
                    request,
                    f"Your household profile {house_form_instance.name}"
                    f" has been created on"
                    f" {datetime.datetime.today().strftime('%b %d, %Y, %H:%M:%S')}")
                return redirect(reverse(index))
    house_form = HouseholdForm()
    member_formset = MemberFormSet(prefix="member")
    return render(request, 'mykitchen/register_household.template.html', {
        'house_form': house_form,
        'member_form': member_formset
    })


@login_required
@permission_required(['mykitchen.view_household',
                      'mykitchen.add_household',
                      'mykitchen.change_household',
                      'mykitchen.view_member',
                      'mykitchen.add_member',
                      'mykitchen.change_member'])
def edit_household(request, household_id):
    household_to_update = get_object_or_404(Household, pk=household_id)
    current_members = Member.objects.filter(household=household_to_update)
    household_members = [x.user for x in current_members]
    if request.method == 'POST':
        edit_house_form = HouseholdForm(request.POST,
                                        instance=household_to_update)
        edit_member_form = MemberFormSet(request.POST,
                                         instance=household_to_update,
                                         prefix="member")
        if edit_house_form.is_valid():
            edit_house_form.save(commit=False)
            edit_house_form.owner = request.user
            if edit_member_form.is_valid():
                edit_member_form.save(commit=False)
                edited_form_members = []
                for new_member in edit_member_form.cleaned_data:
                    if new_member.get('user'):
                        edited_form_members.append(new_member.get('user'))
                    else:
                        pass
                removed_members = [
                    p for p in household_members if p not in
                    edited_form_members]
                added_members = [
                    p for p in edited_form_members if p not in
                    household_members]
                check_for_membership = []
                for member in added_members:
                    try:
                        member = Member.objects.get(user=member)
                    except Member.DoesNotExist:
                        member = None
                    check_for_membership.append(member)
                if all(x is None for x in check_for_membership):
                    member_group = Group.objects.get(name='member_group')
                    member_group.user_set.remove(*removed_members)
                    member_group.user_set.add(*added_members)
                    # save the household object
                    edit_house_form.save()
                    # save the members
                    edit_member_form.save()
                    household_name = edit_house_form.cleaned_data["name"]
                    messages.success(
                        request,
                        f"Your household profile {household_name}"
                        f" has been edited on"
                        f" {datetime.datetime.today().strftime('%b %d, %Y, %H:%M:%S')}")
                    return redirect(reverse(index))
    edit_house_form = HouseholdForm(instance=household_to_update)
    edit_member_form = MemberFormSet(instance=household_to_update,
                                     prefix="member")
    return render(request, 'mykitchen/update_household.template.html', {
                  'house_form': edit_house_form,
                  'member_form': edit_member_form
                  })


@login_required
@permission_required(['mykitchen.delete_household',
                      'mykitchen.delete_member'])
def delete_household(request, household_id):
    household_to_delete = get_object_or_404(Household, pk=household_id)
    owner = household_to_delete.owner
    current_members = [x.user for x in Member.objects.filter(
        household=household_to_delete)]
    if request.method == 'POST':
        owner_group = Group.objects.get(name='owner_group')
        member_group = Group.objects.get(name='member_group')
        owner_group.user_set.remove(owner)
        member_group.user_set.remove(*current_members)
        household_to_delete.delete()
        messages.success(
            request,
            f"{household_to_delete}"
            f" has been deleted from the system, on"
            f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
        return redirect(reverse(index))
