from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from .forms import (HouseholdForm, MemberFormSet, StorageLocationForm,
                    FoodItemForm)
from .models import Member, Household, StorageLocation, FoodItem
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
import datetime
from django.db.models import Q
from django.http import Http404
from django.core.exceptions import PermissionDenied

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

    # if household exists for request.user, and user matches the
    # username of owner or member, set belongs to True
    if household:
        if user.username == household.owner.username or (
                            user.username == member.user.username):
            belongs = True

    # get all storage that belongs to user's household
    # get all foods in the storages
    try:
        storages = StorageLocation.objects.filter(household=household)
    except StorageLocation.DoesNotExist:
        storages = None

    all_food = FoodItem.objects.filter(location__in=storages)
    store_data = {}
    for store in storages:
        foods = FoodItem.objects.filter(
            location__name__iexact=str(store)).count()
        store_data[store] = foods

    # if household is None, set it to empty string for flash msg
    if household is None:
        household = ""
        messages.info(
            request,
            "Please register the household and link the members."
        )

    return render(request, 'mykitchen/mykitchen_index.template.html', {
        'household': household,
        'all_food': all_food,
        'store_data': store_data,
        'belongs': belongs
    })


"""
My Kitchen App Manage(View) Household Profile Page
Purpose: Page to allow household owners to view the household information
they have registered.
1. Get the household by household id
2. Get the members of the household
3. If household exists, check user is household owner
4. If true, renders template
5. If false, raise Permission Denied
6. Raise 404 if Household does not exists
"""


@login_required
@permission_required(['mykitchen.view_household',
                      'mykitchen.view_member'])
def view_household(request, household_id):
    user = request.user
    household = get_object_or_404(Household, pk=household_id)
    members = Member.objects.filter(household=household)
    if household:
        if user.username == household.owner.username:
            return render(request,
                          'mykitchen/view_household.template.html', {
                           'household': household,
                           'members': members
                          })
        else:
            raise PermissionDenied
    else:
        raise Http404


"""
My Kitchen App Manage Register Household Profile Page
Purpose: Page to allow household owners to register household information
1. Filter the form queryset to show only users that do not belong to
   any households, are not owners, and not admin
2. Serve the form on GET request
3. On request == POST, add owners to group = "owner_group" for permissions
4. If form is valid, save the household name to database.
5. If member formset is valid,
6. Check if user does not exists or already is a member of another household
7. Flash error if there is an error
8. Otherwise, add user to group = "member_group", save the members information
9. Flash success message and render template
"""


@login_required
def register_household(request):
    all_existing_members = Member.objects.all()
    # get the id of the household owners
    owners_pk = [h.owner.id for h in Household.objects.all()]
    # list the ids of all household members
    all_members_pk = [am.user.id for am in all_existing_members]
    # generate the list of users to be excluded (household owners and
    # other existing household members) including admin (id=1) and
    # request.user
    to_be_excluded = [1, *owners_pk, *all_members_pk, request.user.id]
    house_form = HouseholdForm()
    member_formset = MemberFormSet(prefix="member")
    # overwrite the queryset in each member formset
    for formsets in member_formset.forms:
        formsets.fields['user'].queryset = (
            formsets.fields['user'].queryset.exclude(Q(id__in=to_be_excluded)))
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
    return render(request, 'mykitchen/register_household.template.html', {
        'house_form': house_form,
        'member_form': member_formset
    })


"""
My Kitchen App Edit Household Profile Page
Purpose: Page to allow household owners to edit household information
1. Filter the form queryset to show only users that do not belong to
   other households, are not owners, and not admin
2. Serve the form on GET request
3. On request == POST, get the list of members
4. Get the list of added members and list of removed members
5. Check for membership in list of added members
6. If any in list is has no membership, added the members to member_group
7. Remove the removed members from member_group
8. Save the data into the database
9. Flash success message and render template
"""


@login_required
@permission_required(['mykitchen.view_household',
                      'mykitchen.add_household',
                      'mykitchen.change_household',
                      'mykitchen.view_member',
                      'mykitchen.add_member',
                      'mykitchen.change_member'])
def edit_household(request, household_id):
    user = request.user
    household_to_update = get_object_or_404(Household, pk=household_id)
    current_members = Member.objects.filter(household=household_to_update)
    if household_to_update:
        if user.username == household_to_update.owner.username:
            # get the id of the household owners
            owners_pk = [h.owner.id for h in Household.objects.all()]
            # list the current household members
            household_members = [x.user for x in current_members]
            # get members of other households
            other_members = Member.objects.exclude(user__in=household_members)
            # list the id of the members of other households
            other_members_pk = [om.user.id for om in other_members]
            # generate the list of users to be excluded (household owners and
            # other existing household members) including admin (id=1)
            to_be_excluded = [1, *owners_pk, *other_members_pk]
            # create the form and populate with object instance
            edit_house_form = HouseholdForm(instance=household_to_update)
            edit_member_form = MemberFormSet(instance=household_to_update,
                                             prefix="member")
            # overwrite the queryset in each member formset
            for formsets in edit_member_form.forms:
                formsets.fields['user'].queryset = (
                    formsets.fields['user'].queryset.exclude(
                        Q(id__in=to_be_excluded)))
            if request.method == 'POST':
                edit_house_form = HouseholdForm(request.POST,
                                                instance=household_to_update)
                edit_member_form = MemberFormSet(request.POST,
                                                 instance=household_to_update,
                                                 prefix="member")
                if edit_house_form.is_valid():
                    edit_house_form.save(commit=False)
                    # set household owner to request.user
                    edit_house_form.owner = request.user
                    if edit_member_form.is_valid():
                        edit_member_form.save(commit=False)
                        # get a list of edited members
                        edited_form_members = []
                        for new_member in edit_member_form.cleaned_data:
                            if new_member.get('user'):
                                edited_form_members.append(
                                    new_member.get('user'))
                            else:
                                pass
                        # get the removed members
                        removed_members = [
                            p for p in household_members if p not in
                            edited_form_members]
                        # get the added members
                        added_members = [
                            p for p in edited_form_members if p not in
                            household_members]
                        # check if the added members have household
                        # membership
                        check_for_membership = []
                        for member in added_members:
                            try:
                                member = Member.objects.get(user=member)
                            except Member.DoesNotExist:
                                member = None
                            check_for_membership.append(member)
                        # if any of the added members are not existing
                        # members,add them to member_group and remove
                        # old members
                        if any(x is None for x in check_for_membership):
                            member_group = Group.objects.get(
                                name='member_group')
                            member_group.user_set.remove(*removed_members)
                            member_group.user_set.add(*added_members)
                        # save the household object
                        edit_house_form.save()
                        # save the members
                        edit_member_form.save()
                        # for flash messaging display only
                        household_name = edit_house_form.cleaned_data[
                            "name"]
                        messages.success(
                            request,
                            f"Your household profile {household_name}"
                            f" has been edited on"
                            f" {datetime.datetime.today().strftime('%b %d, %Y, %H:%M:%S')}")
                    return redirect(reverse(index))
                else:
                    return render(request,
                                  'mykitchen/update_household.template.html', {
                                   'house_form': edit_house_form,
                                   'member_form': edit_member_form
                                  })
            else:
                return render(request,
                              'mykitchen/update_household.template.html', {
                               'house_form': edit_house_form,
                               'member_form': edit_member_form
                              })
        else:
            raise PermissionDenied
    else:
        raise Http404


"""
My Kitchen App Delete Household Profile Page
Purpose: Page to allow household owners to delete household information
1. Get requested household by id
2. Get the owner from household.owner
3. Get all the current members
4. On request == POST, remove all members and owners from respective group
5. Delete data from database
6. Flash success message and render template
"""


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


"""
My Kitchen App View All Storage Page
Purpose: Page to allow household members to view all storage in their homes
1. If household exists, check user matches owner
2. If true, renders template
3. If false, if membership exists,
4. Check user's household matches household to view
5. If true, renders template
6. If false, raise PermissionDenied
"""


@login_required
@permission_required(['mykitchen.view_storagelocation',
                      'mykitchen.add_storagelocation'])
def view_storage_location(request, household_id):
    user = request.user
    household = get_object_or_404(Household, pk=household_id)
    storage = StorageLocation.objects.filter(household=household)
    # get user household membership
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    if household:
        if user.username == household.owner.username:
            return render(request,
                          'mykitchen/view_storage_location.template.html', {
                              'storage': storage,
                              'household': household
                          })
        elif member:
            if member.household == household:
                return render(
                    request,
                    'mykitchen/view_storage_location.template.html', {
                        'storage': storage,
                        'household': household
                    })
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied
    else:
        raise Http404


"""
My Kitchen App View Add Storage Page
Purpose: Page to allow household members to add storage locations info
1. If household exists, check user matches owner
2. If true, if method = POST, process and save information
3. If true, if method = GET, renders form
4. If false, if user is a household member,
5. if method = POST, process and save information
6. if method = GET, renders form
7. If user is neither household owner nor member,
8. Raise PermissionDenied
9. If household does not exists, return status 404.
"""


@login_required
@permission_required(['mykitchen.add_storagelocation',
                      'mykitchen.change_storagelocation'])
def add_storage_location(request, household_id):
    user = request.user
    household = get_object_or_404(Household, pk=household_id)
    new_storage_form = StorageLocationForm()
    # get user household membership
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    if household:
        if user.username == household.owner.username:
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
                # if request = GET
                return render(
                    request, 'mykitchen/input_storage.template.html', {
                        'form': new_storage_form,
                        'household': household
                            })
        elif member:
            if member.household == household:
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
                else:  # if request = GET
                    return render(request,
                                  'mykitchen/input_storage.template.html', {
                                    'form': new_storage_form,
                                    'household': household
                                    })
            else:
                raise PermissionDenied
    else:
        raise Http404


"""
My Kitchen App View Update Storage Page
Purpose: Page to allow household members to edit storage locations info
1. If household exists, check user matches owner
2. If true, if method = POST, process and save information
3. If true, if method = GET, renders form
4. If false, if user is a household member,
5. if method = POST, process and save information
6. if method = GET, renders form
7. If user is neither household owner nor member,
8. Raise PermissionDenied
9. If household does not exists, return status 404.
"""


@login_required
@permission_required(['mykitchen.add_storagelocation',
                      'mykitchen.change_storagelocation'])
def update_storage_location(request, household_id, storage_id):
    user = request.user
    storage_to_update = get_object_or_404(StorageLocation, pk=storage_id)
    household = get_object_or_404(Household, pk=household_id)
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    if household:
        if user.username == household.owner.username:
            if request.method == 'POST':
                edit_storage_form = StorageLocationForm(
                    request.POST, instance=storage_to_update)
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
                    # if form is not valid
                    return render(request,
                                  'mykitchen/update_storage.template.html', {
                                   'form': edit_storage_form,
                                   'household': household
                                  })
            else:
                edit_storage_form = (
                    StorageLocationForm(instance=storage_to_update))
                return render(request,
                              'mykitchen/update_storage.template.html', {
                               'form': edit_storage_form,
                               'household': household
                                    })
        elif member:
            if member.household == household:
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
                        # if form is not valid
                        return render(
                            request,
                            'mykitchen/update_storage.template.html', {
                             'form': edit_storage_form,
                             'household': household
                             })
                else:
                    edit_storage_form = (
                        StorageLocationForm(instance=storage_to_update))
                    return render(
                        request,
                        'mykitchen/update_storage.template.html', {
                         'form': edit_storage_form,
                         'household': household
                        })
            else:
                raise PermissionDenied
    else:
        raise Http404


"""
My Kitchen App View Delete Storage Page
Purpose: Page to allow household members to edit storage locations info
1. Check storage to delete, and household
2. If household exists, check user matches owner
3. If true, if method = POST, process delete storage
4. If false, if user is a household member,
5. if method = POST, process delete storage
6. If user is neither household owner nor member,
7. Raise PermissionDenied
8. If household does not exists, return status 404.
"""


@login_required
@permission_required(['mykitchen.change_storagelocation',
                      'mykitchen.delete_storagelocation'])
def delete_storage_location(request, household_id, storage_id):
    user = request.user
    storage_to_delete = get_object_or_404(StorageLocation, pk=storage_id)
    household = get_object_or_404(Household, pk=household_id)
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    if household:
        if user.username == household.owner.username:
            if request.method == 'POST':
                storage_to_delete.delete()
                messages.success(
                    request,
                    f"{storage_to_delete}"
                    f" has been deleted, on"
                    f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
                return redirect(reverse(index))
        elif member:
            if member.household == household:
                if request.method == 'POST':
                    storage_to_delete.delete()
                    messages.success(
                        request,
                        f"{storage_to_delete}"
                        f" has been deleted, on"
                        f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
                    return redirect(reverse(index))
        else:
            raise PermissionDenied
    else:
        return Http404


"""
My Kitchen App View Storage Content Page
Purpose: Page to allow household members to view food items in storage
1. Get household, storage and food items in storage
2. If household exists, check user matches owner
3. If true, renders template
4. If false, if user is a household member,
5. Renders template
6. If user is neither household owner nor member,
7. Raise PermissionDenied
8. If household does not exists, return status 404.
"""


@login_required
@permission_required('mykitchen.view_fooditem')
def storage_content_view(request, household_id, storage_id):
    user = request.user
    household = get_object_or_404(Household, pk=household_id)
    storage = get_object_or_404(StorageLocation, pk=storage_id)
    # there's a bug here. for postgresql, need to be a string
    stored_food = FoodItem.objects.filter(location__name__iexact=str(storage))
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    if household:
        if user.username == household.owner.username:
            return render(request,
                          'mykitchen/view_storage_content.template.html', {
                           'storage': storage,
                           'household': household,
                           'stored_food': stored_food
                          })
        elif member:
            if member.household == household:
                return render(request,
                              'mykitchen/view_storage_content.template.html', {
                               'storage': storage,
                               'household': household,
                               'stored_food': stored_food
                              })
            else:
                raise PermissionDenied
    else:
        return Http404


"""
My Kitchen App Add Storage Content Page
Purpose: Page to allow household members to add food items in storage
1. Get household and storage by id
2. If household exists, check user matches owner
3. If true, renders form if method = GET
4. Else if method = POST, process and save the data
5. If false, if user is a household member,
6. Renders form if method = GET
7. If method = POST, process and save the data
8. If user is neither household owner nor member,
9. Raise PermissionDenied
10. If household does not exists, return status 404.
"""


@login_required
@permission_required('mykitchen.add_fooditem')
def add_food_item(request, household_id, storage_id):
    user = request.user
    storage = get_object_or_404(StorageLocation, pk=storage_id)
    household = get_object_or_404(Household, pk=household_id)
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    if household:
        if user.username == household.owner.username:
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
                    return render(request,
                                  'mykitchen/input_food.template.html', {
                                   'form': food_form,
                                   'household': household
                                  })
            else:
                food_form = FoodItemForm()
                return render(request, 'mykitchen/input_food.template.html', {
                    'form': food_form,
                    'household': household
                })
        elif member:
            if member.household == household:
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
                        return render(request,
                                      'mykitchen/input_food.template.html', {
                                       'form': food_form,
                                       'household': household
                                      })
                else:
                    food_form = FoodItemForm()
                    return render(request,
                                  'mykitchen/input_food.template.html', {
                                   'form': food_form,
                                   'household': household
                                  })
            else:
                raise PermissionDenied
    else:
        return Http404


"""
My Kitchen App Update Storage Content Page
Purpose: Page to allow household members to update food items info in storage
1. Get household, storage and food item by id
2. If household exists, check user matches owner
3. If true, renders form if method = GET
4. Else if method = POST, process and save the data
5. If false, if user is a household member,
6. Renders form if method = GET
7. If method = POST, process and save the data
8. If user is neither household owner nor member,
9. Raise PermissionDenied
10. If household does not exists, return status 404.
"""


@login_required
@permission_required('mykitchen.change_fooditem')
def edit_food_item(request, household_id, storage_id, food_id):
    user = request.user
    storage = get_object_or_404(StorageLocation, pk=storage_id)
    household = get_object_or_404(Household, pk=household_id)
    food_to_edit = FoodItem.objects.get(id=food_id)
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    if household:
        if user.username == household.owner.username:
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
                    return render(request,
                                  'mykitchen/update_food.template.html', {
                                   'form': food_form,
                                   'household': household
                                  })
            else:
                food_form = FoodItemForm(instance=food_to_edit)
                return render(request, 'mykitchen/update_food.template.html', {
                    'form': food_form,
                    'household': household
                })
        elif member:
            if member.household == household:
                if request.method == 'POST':
                    food_form = FoodItemForm(request.POST,
                                             instance=food_to_edit)
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
                        return render(request,
                                      'mykitchen/update_food.template.html', {
                                       'form': food_form,
                                       'household': household
                                      })
                else:
                    food_form = FoodItemForm(instance=food_to_edit)
                    return render(request,
                                  'mykitchen/update_food.template.html', {
                                   'form': food_form,
                                   'household': household
                                  })
            else:
                raise PermissionDenied
    else:
        return Http404


"""
My Kitchen App Update Storage Content Page
Purpose: Page to allow household members to update food items info in storage
1. Get household and food item by id
2. If household exists, check user matches owner
3. If true, renders form if method = GET
4. Else if method = POST, process and save the data
5. If false, if user is a household member,
6. Renders form if method = GET
7. If method = POST, process and save the data
8. If user is neither household owner nor member,
9. Raise PermissionDenied
10. If household does not exists, return status 404.
"""


@login_required
@permission_required('mykitchen.delete_fooditem')
def delete_food_item(request, household_id, storage_id, food_id):
    user = request.user
    household = get_object_or_404(Household, pk=household_id)
    food_to_delete = FoodItem.objects.get(id=food_id)
    try:
        member = Member.objects.get(user=user)
    except Member.DoesNotExist:
        member = None
    if household:
        if user.username == household.owner.username:
            if request.method == 'POST':
                food_to_delete.delete()
                messages.success(
                    request,
                    f"{food_to_delete} has been deleted from"
                    f" {food_to_delete.location.name} on"
                    f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
                return redirect(reverse(index))
        elif member:
            if member.household == household:
                if request.method == 'POST':
                    food_to_delete.delete()
                    messages.success(
                        request,
                        f"{food_to_delete} has been deleted from"
                        f" {food_to_delete.location.name} on"
                        f" {datetime.datetime.now().strftime('%b %d, %Y, %H:%M:%S')}")
                    return redirect(reverse(index))
            else:
                raise PermissionDenied
    else:
        return Http404
