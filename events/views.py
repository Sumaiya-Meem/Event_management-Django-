from django.shortcuts import render, redirect
from django.contrib import messages
from events.models import Event, Category, Participant
from events.form import EventModelForm, CategoryModelForm, ParticipantModelForm,ParticipantForm


# Create your views here.

def home_page(request):
    return render(request,"home.html")

def event_page(request):
    return render(request,"event.html")

def admin_dashboard(request):
    return render(request,"dashboard.html")

def admin_home(request):
        context = {
        'section': 'admin_home',
        }
        return render(request,'admin_page.html',context )


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

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category created successfully!")
            return redirect('create-category')

    context = {
        'category_form': category_form,
        'section': 'create_category'
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



