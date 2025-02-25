from django.shortcuts import render, redirect
from django.contrib import messages
from events.models import *
from events.form import EventModelForm, CategoryModelForm, ParticipantModelForm,ParticipantForm
from django.db.models import Count,Q
from datetime import datetime

def home_page(request):
    categories = Category.objects.all()
    selected_category_id = request.GET.get('category', 'all')
    
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    
    if selected_category_id and selected_category_id != 'all':
        events = events.filter(category_id=selected_category_id)
    
    # Search functioality
    keyword = request.GET.get('keyword')
    if keyword:
        events = events.filter(Q(name__icontains=keyword) | Q(location__icontains=keyword)
        )
    
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        events = events.filter(date__gte=start_date)
    
    if end_date:
        events = events.filter(date__lte=end_date)
    
    context = {
        'events': events,
        'categories': categories,
        'selected_category_id': selected_category_id,
    }
    return render(request, 'home.html', context)





def event_page(request):
    
    
    return render(request, "event.html")

def event_detail(request,id):
    event = Event.objects.select_related('category').prefetch_related('participants').get(id=id)
    
    context = {
        'event': event,
    }
    return render(request, 'event_detail.html', context)

def admin_dashboard(request):
   
    return render(request, "dashboard.html",)




def admin_home(request):
    total_event = Event.objects.count()

   
    total_participants = Event.objects.aggregate(total=Count('participants', distinct=True))


    upcoming_events = Event.objects.filter(date__gte=datetime.now().date()).count()

   
    past_events = Event.objects.filter(date__lte=datetime.now().date()).count()

   
    event_filter = request.GET.get('event', 'all')
    if event_filter == 'upcoming':
        events = Event.objects.filter(date__gte=datetime.now().date())
    elif event_filter == 'past':
        events = Event.objects.filter(date__lte=datetime.now().date())
    else:
        events = Event.objects.all()

    context = {
        'total_event': total_event,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'events': events,  
        'event_filter': event_filter,  
    }
    return render(request, 'admin_page.html', context)


def create_event(request):
                  
    event_form = EventModelForm()
    participant_form = ParticipantModelForm()

    if request.method == 'POST':

        event_form = EventModelForm(request.POST)
        participant_form = ParticipantModelForm(request.POST)

     
        if event_form.is_valid() and participant_form.is_valid():
    
            event = event_form.save()

           
            participants = participant_form.cleaned_data['participants']
            event.participants.set(participants)

            
            messages.success(request, "Event created successfully!")
            return redirect('create-event') 

    
    context = {
        'event_form': event_form,
        'participant_form': participant_form,
        'section': 'create_event',
    }

    return render(request, 'event_form.html', context)


def create_category(request):
    category_form = CategoryModelForm()
    catgories=Category.objects.all()

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category created successfully!")
            return redirect('create-category')

    context = {
        'category_form': category_form,
        'catgories': catgories,
        'section': 'create_category',
    }
    return render(request, 'create_categoryForm.html', context)   

def create_participant(request):
                  
    participant_form = ParticipantForm()
    print(participant_form)

    if request.method == 'POST':

        participant_form = ParticipantForm(request.POST)

     
        if participant_form.is_valid():
            participant_form.save()
            
            messages.success(request, "Participant created successfully!")
            return redirect('create-participant') 

    
    context = {
        'participant_form': participant_form,
        'section': 'create_participant'
    }

    return render(request, 'add_participant.html', context)



