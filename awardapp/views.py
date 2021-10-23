from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import *
import datetime as dt
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
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

def get_project_by_id(request, id):

    try:
        project = Projects.objects.get(pk = id)
        
    except Projects.ObjectDoesNotExist:
        raise Http404()    
    
    return render(request, "project.html", {"project":project})

@login_required(login_url='login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = current_user
            form.save()
        return redirect('/')

    else:
        form = NewProjectForm()
    return render(request, 'new_project.html', {"form":form})
