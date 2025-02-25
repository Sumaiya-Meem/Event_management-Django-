from django.shortcuts import render, redirect
from django.contrib import messages
from events.models import *
from events.form import EventModelForm, CategoryModelForm, ParticipantModelForm,ParticipantForm
from django.db.models import Count,Q
from datetime import datetime, date

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
    participants=Participant.objects.all()
    

    if request.method == 'POST':

        participant_form = ParticipantForm(request.POST)

     
        if participant_form.is_valid():
            participant_form.save()
            
            messages.success(request, "Participant created successfully!")
            return redirect('create-participant') 

    
    context = {
        'participant_form': participant_form,
        'participants': participants,
        'section': 'create_participant'
    }

    return render(request, 'add_participant.html', context)



def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event) 
    
    participant_form = ParticipantModelForm(initial={'participants': event.participants.all()}) 

    if request.method == 'POST':
        event_form = EventModelForm(request.POST, instance=event) 
        participant_form = ParticipantModelForm(request.POST) 

        if event_form.is_valid() and participant_form.is_valid():
            event = event_form.save() 


            participants = participant_form.cleaned_data['participants']
            event.participants.set(participants)

            messages.success(request, "Event updated successfully!")
            return redirect('update-event', id) 

    else:
        event_form = EventModelForm(instance=event)  

    context = {
        'event_form': event_form,
        'participant_form': participant_form,
        'section': 'update_event',
    }
    return render(request, 'event_form.html', context)


def update_category(request,id):
    catgory=Category.objects.get(id=id)
    category_form = CategoryModelForm(instance=catgory)

    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST, instance=catgory) 
        if category_form.is_valid():
            category_form.save()  
            messages.success(request, "Category updated successfully!")
            return redirect('create-category')  

    context = {
        'category_form': category_form,
        'section': 'update_category',
    }
    return render(request, 'create_categoryForm.html', context)      

def update_participant(request,id):
    participant=Participant.objects.get(id=id)
    participant_form = ParticipantForm(instance=participant)

    if request.method == 'POST':
        participant_form = ParticipantForm(request.POST, instance=participant) 
        if participant_form.is_valid():
            participant_form.save()  
            messages.success(request, "Participant updated successfully!")
            return redirect('create-participant')  

    context = {
        'participant_form': participant_form,
        'section': 'create_participant',
    }
    return render(request, 'add_participant.html', context)     
 


def delete_event(request,id):
   if request.method=='POST':
      event=Event.objects.get(id=id)
      event.delete()
      
      messages.success(request,'Event deleted successfully')
      return redirect('admin-home')
   else:
    messages.error(request,"Something went wrong")
    return redirect('admin-home')



def delete_category(request,id):
   if request.method=='POST':
      category=Category.objects.get(id=id)
      category.delete()
      
      messages.success(request,'Category deleted successfully')
      return redirect('create-category')
   else:
    messages.error(request,"Something went wrong")
    return redirect('create-category')

def delete_participant(request,id):
   if request.method=='POST':
      participant=Participant.objects.get(id=id)
      participant.delete()
      
      messages.success(request,'Participant deleted successfully')
      return redirect('create-participant')
   else:
    messages.error(request,"Something went wrong")
    return redirect('create-participant')




