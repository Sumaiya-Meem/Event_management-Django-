from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def home_page(request):
    return render(request,"home.html")

def event_page(request):
    return render(request,"event.html")

def admin_dashboard(request):
    return render(request,"dashboard.html")