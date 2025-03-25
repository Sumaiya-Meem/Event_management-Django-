from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def no_permission(request):
    return render(request,'no_permission.html')