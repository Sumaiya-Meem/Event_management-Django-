from django.db import models
from django.contrib.auth.models import User
# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.name


# Event Model
class Event(models.Model):
    name = models.CharField(max_length=200) 
    description = models.TextField() 
    date = models.DateField() 
    time = models.TimeField() 
    location = models.CharField(max_length=200) 
    asset = models.ImageField(upload_to='tasks_asset',  blank=True, null=True,default="tasks_asset/img1.jpeg")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events') 
    participants = models.ManyToManyField(User, related_name='event_rsvp', blank=True) 

    def __str__(self):
        return self.name

class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} RSVPed to {self.event.name}"
    
# Participant Model
# class Participant(models.Model):
#     name = models.CharField(max_length=100)  
#     email = models.EmailField(unique=True)  
#     events = models.ManyToManyField(Event, related_name='participants') 

#     def __str__(self):
#         return self.name
