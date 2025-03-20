from django.shortcuts import render,redirect
from users.forms import CustomRegisterForm
from django.contrib import messages
from django.contrib.auth import login,logout
# Create your views here.
def sign_up(request):
    form = CustomRegisterForm()
    if request.method=='POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request, "Registration successful! Welcome aboard 🎉")
            return redirect('home')
        else:
            print("Form is not valid")
            
    context = {'form': form}               
    return render(request,'registration/register.html',context)

def sign_in(request):
   return render(request,'registration/login.html')


def log_out(request):
   if request.method=='POST':
      logout(request)
      return redirect('home')