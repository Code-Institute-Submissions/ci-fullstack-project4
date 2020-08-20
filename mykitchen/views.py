from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import (HouseholdForm, MemberFormSet, StorageLocationForm,
                    FoodItemForm)
from .models import Member, Household, StorageLocation, FoodItem
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
import datetime

# Create your views here.

"""
My Kitchen App Index Page.
Purpose: Landing page to receive store customers and to link them to the app
that manages their kitchen inventory
"""


@login_required
def index(request):
    # get user = request.user,
    user = request.user
    # set belongs to False by default
    belongs = False

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

    # if household is None, set it to empty string and flash msg
    if household is None:
        household = ""
        messages.info(
            request,
            "Please register the household and link the members."
        )

    # if household exists for request.user, and user matches the
    # username of owner or member, set belongs to True
    if household:
        if user.username == household.owner.username or (
                            user.username == member.user.username):
            belongs = True

    # get all storage that belongs to user's household
    # get all foods in the storages
    storages = StorageLocation.objects.filter(household=household)
    all_food = FoodItem.objects.filter(location__in=storages)

    for food in all_food:
        print(food.food.name,food.get_expired(), food.get_hit_threshold())
    return render(request, 'mykitchen/mykitchen_index.template.html', {
        'household': household,
        'all_food': all_food,
        'belongs': belongs
    })


"""
My Kitchen App Manage(View) Household Profile Page
Purpose: Page to allow household owners to view the household information
they have registered.
1. Get the household by household id
2. Get the members of the household
3. Render the template
"""


@login_required
@permission_required(['mykitchen.view_household',
                      'mykitchen.view_member'])
def view_household(request, household_id):
    household = Household.objects.get(id=household_id)
    members = Member.objects.filter(household=household)
    return render(request, 'mykitchen/view_household.template.html', {
        'household': household,
        'members': members
    })


@login_required
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


def view_storage_location(request, household_id):
    household = Household.objects.get(id=household_id)
    storage = StorageLocation.objects.filter(household=household)
    return render(request, 'mykitchen/view_storage_location.template.html', {
        'storage': storage,
        'household': household
    })


def add_storage_location(request, household_id):
    household = Household.objects.get(id=household_id)
    if request.method == 'POST':
        new_storage_form = StorageLocationForm(request.POST)
        # if the form is validated
        if new_storage_form.is_valid():
            storage_instance = new_storage_form.save(commit=False)
            storage_instance.edited_by = request.user
            storage_instance.household = household
            storage_instance.save()
            messages.success(
                request,
                f"New Storage {storage_instance.name}"
                f" has been created on"
                f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
            return redirect(reverse(index))
        else:
            return render(request, 'mykitchen/input_storage.template.html', {
                          'form': new_storage_form
                          })
    else:
        new_storage_form = StorageLocationForm()
        return render(request, 'mykitchen/input_storage.template.html', {
            'form': new_storage_form
        })


def update_storage_location(request, household_id, storage_id):
    storage_to_update = StorageLocation.objects.get(id=storage_id)
    household = Household.objects.get(id=household_id)
    if request.method == 'POST':
        edit_storage_form = StorageLocationForm(request.POST,
                                                instance=storage_to_update)
        # if the form is validated
        if edit_storage_form.is_valid():
            storage_instance = edit_storage_form.save(commit=False)
            storage_instance.edited_by = request.user
            storage_instance.household = household
            storage_instance.save()
            messages.success(
                request,
                f"Storage {storage_instance.name}"
                f" has been updated on"
                f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
            return redirect(reverse(index))
        else:
            return render(request, 'mykitchen/update_storage.template.html', {
                          'form': edit_storage_form
                          })
    else:
        edit_storage_form = StorageLocationForm(instance=storage_to_update)
        return render(request, 'mykitchen/update_storage.template.html', {
            'form': edit_storage_form
        })


def delete_storage_location(request, household_id, storage_id):
    storage_to_delete = StorageLocation.objects.get(id=storage_id)
    if request.method == 'POST':
        storage_to_delete.delete()
        messages.success(
            request,
            f"{storage_to_delete}"
            f" has been deleted, on"
            f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
        return redirect(reverse(index))


def storage_content_view(request, household_id, storage_id):
    household = Household.objects.get(id=household_id)
    storage = StorageLocation.objects.get(id=storage_id)
    stored_food = FoodItem.objects.filter(location__name__iexact=storage)
    return render(request, 'mykitchen/view_storage_content.template.html', {
        'storage': storage,
        'household': household,
        'stored_food': stored_food
    })


def add_food_item(request, household_id, storage_id):
    storage = StorageLocation.objects.get(id=storage_id)
    if request.method == 'POST':
        food_form = FoodItemForm(request.POST)
        if food_form.is_valid():
            food_instance = food_form.save(commit=False)
            food_instance.edited_by = request.user
            food_instance.location = storage
            food_instance.save()
            messages.success(
                request,
                f"New Food Item {food_instance.food}"
                f" has been added on"
                f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
            return redirect(reverse(index))
        else:
            return render(request, 'mykitchen/input_food.template.html', {
                          'form': food_form
                          })
    else:
        food_form = FoodItemForm()
        return render(request, 'mykitchen/input_food.template.html', {
            'form': food_form
        })


def edit_food_item(request, household_id, storage_id, food_id):
    storage = StorageLocation.objects.get(id=storage_id)
    food_to_edit = FoodItem.objects.get(id=food_id)
    if request.method == 'POST':
        food_form = FoodItemForm(request.POST, instance=food_to_edit)
        if food_form.is_valid():
            food_instance = food_form.save(commit=False)
            food_instance.edited_by = request.user
            food_instance.location = storage
            food_instance.save()
            messages.success(
                request,
                f" Food Item {food_instance.food}"
                f" has been edited on"
                f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
            return redirect(reverse(index))
        else:
            return render(request, 'mykitchen/update_food.template.html', {
                          'form': food_form
                          })
    else:
        food_form = FoodItemForm(instance=food_to_edit)
        return render(request, 'mykitchen/update_food.template.html', {
            'form': food_form
        })


def delete_food_item(request, household_id, storage_id, food_id):
    food_to_delete = FoodItem.objects.get(id=food_id)
    if request.method == 'POST':
        food_to_delete.delete()
        messages.success(
            request,
            f"{food_to_delete} has been deleted from"
            f" {food_to_delete.location.name} on"
            f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
        return redirect(reverse(index))
