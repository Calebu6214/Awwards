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

class ProjectsList(APIView):
    def get(self, request, format=None):
        all_merch = Projects.objects.all()
        serializers = ProjectsSerializer(all_merch, many=True)
        return Response(serializers.data)

 
class ProfileList(APIView):
    def get(self, request, format=None):
        all_merch = Profile.objects.all()
        serializers = ProfileSerializer(all_merch, many=True)
        return Response(serializers.data)

class ProjectsDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_projects(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            return Http404
        
    def get(self, request, pk, format=None):
        project = self.get_projects(pk)
        serializers = ProjectsSerializer(project)
        return Response(serializers.data)
    
    def put(self, request, pk, format=None):
        project = self.get_projects(pk)
        serializers = ProjectsSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        project = self.get_projects(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

@login_required(login_url='login/')
def search_projects(request):
    if 'keyword' in request.GET and request.GET["keyword"]:
        search_term = request.GET.get("keyword")
        searched_projects = Projects.search_projects(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})

@login_required(login_url='login/')
def user_profiles(request):
    current_user = request.user
    author = current_user
    profile = Profile.objects.filter(user=current_user).first()
    # user_profile = Profile.objects.get(user=request.user)
    projects = Projects.get_by_author(author)
    
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            # form.save(commit=False)
            form.save()
        return redirect('profile')
        
    else:
        form = ProfileUpdateForm() 
        context ={"form":form,
         "projects":projects,
         "profile": profile
         }  
    return render(request, 'django_registration/profile.html', context)
