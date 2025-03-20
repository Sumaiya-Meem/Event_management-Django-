from django.shortcuts import render,redirect
from users.forms import CustomRegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth import login,logout
# Create your views here.

def sign_up(request):
    form = CustomRegisterForm()
    if request.method=='POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            user=form.save(commit=False)
#             print('user',user)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active=False
            user.save()
#             print('user',user)
            messages.success(request, "A Confirmation mail sent. Please check your email")
            return redirect('sign-in')
        else:
            print("Form is not valid")
            
        context = {'form': form}
        return render(request,'registration/register.html',context)



def sign_in(request):
   form=LoginForm()

   if request.method=='POST':
      form=LoginForm(data=request.POST)
      print(form)
      if form.is_valid():
         user=form.get_user()
#          print('user in login',user)
         login(request, user)
         return redirect('home')  
   return render(request,'registration/login.html',{'form':form})


def log_out(request):
   if request.method=='POST':
      logout(request)
      return redirect('home')