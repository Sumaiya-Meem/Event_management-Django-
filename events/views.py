

from django.shortcuts import render, redirect
from django.contrib import messages
from events.models import *
from events.form import (EventModelForm, CategoryModelForm, ParticipantModelForm,
    ParticipantForm, AssignRoleForm, CreateGroupForm
)
from django.http import HttpResponse
from django.db.models import Count, Q
from datetime import date
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required

def is_admin(user):
   return user.groups.filter(name='Admin').exists()

def is_organizer(user):
   return user.groups.filter(name='Organizer').exists()
def is_user(user):
   return user.groups.filter(name='User').exists()


@user_passes_test(is_organizer,login_url='no-permission')
def organizer_dashboard(request):
    total_event = Event.objects.count()
    total_participants = Event.objects.aggregate(total=Count('participants', distinct=True))['total']
    
    # print('total:',total_participants)

    upcoming_events = Event.objects.filter(date__gt=date.today()).count()
    past_events = Event.objects.filter(date__lt=date.today()).count()
    today_events = Event.objects.filter(date=date.today())

    event_filter = request.GET.get('event', '')
    if event_filter == 'upcoming':
        events = Event.objects.filter(date__gt=date.today())
    elif event_filter == 'past':
        events = Event.objects.filter(date__lt=date.today())
    elif event_filter == 'all':
        events = Event.objects.all()
    else:
        events = Event.objects.filter(date=date.today())

    return render(request, 'organizer_home.html', {
        'total_event': total_event,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'events': events,
        'event_filter': event_filter,
    })

@user_passes_test(is_user,login_url='no-permission')
def user_dashboard(request):
   return render(request,"user_dashboard.html")


def home_page(request):
    categories = Category.objects.all()
    selected_category_id = request.GET.get('category', 'all')

    events = Event.objects.select_related('category').prefetch_related('participants').all()

    if selected_category_id != 'all':
        events = events.filter(category_id=selected_category_id)

    keyword = request.GET.get('keyword')
    if keyword:
        events = events.filter(Q(name__icontains=keyword) | Q(location__icontains=keyword))

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    return render(request, 'home.html', {
        'events': events,
        'categories': categories,
        'selected_category_id': selected_category_id,
    })


def event_detail(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'event_detail.html', {'event': event})


def admin_home(request):
    total_event = Event.objects.count()
    total_participants = Event.objects.aggregate(total=Count('participants', distinct=True))['total']
    
    # print('total:',total_participants)

    upcoming_events = Event.objects.filter(date__gt=date.today()).count()
    past_events = Event.objects.filter(date__lt=date.today()).count()
    today_events = Event.objects.filter(date=date.today())

    event_filter = request.GET.get('event', '')
    if event_filter == 'upcoming':
        events = Event.objects.filter(date__gt=date.today())
    elif event_filter == 'past':
        events = Event.objects.filter(date__lt=date.today())
    elif event_filter == 'all':
        events = Event.objects.all()
    else:
        events = Event.objects.filter(date=date.today())

    return render(request, 'admin_page.html', {
        'total_event': total_event,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'events': events,
        'event_filter': event_filter,
    })
    
    
def event_page(request):
    return render(request, "event.html")

@login_required
@permission_required("events.add_event",login_url='no-permission')
def create_event(request):
    event_form = EventModelForm()
    participant_form = ParticipantModelForm()

    if request.method == 'POST':
        event_form = EventModelForm(request.POST,request.FILES)
        participant_form = ParticipantModelForm(request.POST)

        if event_form.is_valid() and participant_form.is_valid():
            event = event_form.save()
            # Correctly associate the participants with the event
            event.participants.set(participant_form.cleaned_data['participants'])
            messages.success(request, "Event created successfully!")
            return redirect('create-event')

    return render(request, 'event_form.html', {
        'event_form': event_form,
        'participant_form': participant_form,
        'section': 'create_event',
    })


@login_required
@permission_required("events.change_event",login_url='no-permission')
def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)
    participant_form = ParticipantModelForm(initial={'participants': event.event_rsvp.all()})

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, instance=event)
        participant_form = ParticipantModelForm(request.POST)

        if event_form.is_valid() and participant_form.is_valid():
            event = event_form.save()
            event.event_rsvp.set(participant_form.cleaned_data['participants'])
            messages.success(request, "Event updated successfully!")
            return redirect('update-event', id)

    return render(request, 'event_form.html', {
        'event_form': event_form,
        'participant_form': participant_form,
        'section': 'update_event',
    })


@login_required
@permission_required("events.delete_event",login_url='no-permission')
def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    messages.success(request, "Event deleted successfully")
    return redirect('admin-home')

@login_required
@permission_required("events.add_category",login_url='no-permission')
def create_category(request):
    category_form = CategoryModelForm()
    categories = Category.objects.all()

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category created successfully!")
            return redirect('create-category')

    return render(request, 'create_categoryForm.html', {
        'category_form': category_form,
        'categories': categories,
        'section': 'create_category',
    })

@login_required
@permission_required("events.change_category",login_url='no-permission')
def update_category(request, id):
    category = Category.objects.get(id=id)
    category_form = CategoryModelForm(instance=category)

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('create-category')

    return render(request, 'create_categoryForm.html', {'category_form': category_form})

@login_required
@permission_required("events.delete_category",login_url='no-permission')
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, "Category deleted successfully")
    return redirect('create-category')

@user_passes_test(is_admin,login_url='no-permission') 
def user_list(request):
    users = User.objects.all()
    return render(request, 'User/userList.html', {"users": users})

@user_passes_test(is_admin,login_url='no-permission') 
def delete_user(request, user_id):
    if request.method == 'POST':
        user = User.objects.filter(id=user_id).first()
        if user:
            user.delete()
            messages.success(request, f"User {user.username} deleted successfully")
        else:
            messages.error(request, "User not found")
    
    return redirect('user-list')

@user_passes_test(is_admin,login_url='no-permission') 
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        role = form.cleaned_data.get('role')
        user.groups.clear()
        user.groups.add(role)
        messages.success(request, f"{user.username} assigned to {role.name} role")
        return redirect('user-list')

    return render(request, 'User/assign_role.html', {'form': form})

@user_passes_test(is_admin,login_url='no-permission') 
def create_group(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully!")
            return redirect('group-list')  
    else:
        form = CreateGroupForm()

    return render(request, 'Group/group_form.html', {'form': form})

@user_passes_test(is_admin,login_url='no-permission') 
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'Group/group_list.html', {'groups': groups})

@user_passes_test(is_admin,login_url='no-permission') 
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    messages.success(request, f"Group {group.name} deleted successfully")
    return redirect('group-list')

@login_required
def rsvp_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)

        if not RSVP.objects.filter(user=request.user, event=event).exists():
            RSVP.objects.create(user=request.user, event=event)

            event.participants.add(request.user)

            messages.success(request, "You have successfully RSVPed for the event.")
            return redirect('event-detail', id=event_id)  
        else:
           
            messages.info(request, "You have already RSVPed for this event.")
            return redirect('event-detail', id=event_id)  
    except Event.DoesNotExist:
        return HttpResponse("Event not found.", status=404)
@login_required
def participant_dashboard(request):
    user = request.user
    events = user.rsvp_set.all().select_related('event') 
    return render(request, 'participant_dashboard.html', {'events': events})

def dashboard(request):
    if is_organizer(request.user):
        return redirect('organizer-dashboard')
    elif is_admin(request.user):
        return redirect('admin-home')
    elif is_user(request.user):
        return redirect('user-dashboard')

    return redirect('no-permission')