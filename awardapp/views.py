from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from . models import *
from django.contrib.auth.forms import UserCreationForm
# from .forms import ProfileForm,CommentsForm, ImageForm
# from .email import send_welcome_email
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form =UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                # messages.success(request,'Account was created successfully')
                return redirect('login')
        context = {'form': form}
        return render(request,'registration/registration_form.html',  context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username ,password=password)
            if user is not None:   
                login(request, user)
        context={'form': form}
        return render(request,'registration/login.html',  context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login/')
def home(request):
    date = dt.date.today()
    projects = Projects.objects.all()
    return render(request, 'index.html', {"date": date,"projects":projects})
