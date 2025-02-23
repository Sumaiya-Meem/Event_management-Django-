from django.shortcuts import render, redirect
from django.contrib import messages
from events.models import Event, Category, Participant
from events.form import EventModelForm, CategoryModelForm, ParticipantModelForm


# Create your views here.

def home_page(request):
    return render(request,"home.html")

def event_page(request):
    return render(request,"event.html")

def admin_dashboard(request):
    return render(request,"dashboard.html")




def create_event(request):
    # Initialize forms
    event_form = EventModelForm()
    participant_form = ParticipantModelForm()

    if request.method == 'POST':
        # Bind forms to POST data
        event_form = EventModelForm(request.POST)
        participant_form = ParticipantModelForm(request.POST)

        # Validate forms
        if event_form.is_valid() and participant_form.is_valid():
            # Save Event
            event = event_form.save()

            # Associate selected participants with the event
            participants = participant_form.cleaned_data['participants']
            event.participants.set(participants)

            # Success message
            messages.success(request, "Event created successfully!")
            return redirect('create-event')  # Redirect to the same page or another page

    # Context for rendering the template
    context = {
        'event_form': event_form,
        'participant_form': participant_form,
    }

    return render(request, 'event_form.html', context)