from django.urls import path,re_path,include
from django.conf.urls import include, url
from django.urls.conf import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    re_path('project/(\d+)', views.get_project_by_id, name='project_results'),
    path('new/project', views.new_project, name='new-project'),
    path('api/projects/', views.ProjectsList.as_view()),
    path('api/profile/', views.ProfileList.as_view()),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('search/', views.search_projects, name='search_results'),
    path('accounts/profile/', views.user_profiles, name='profile'),
    path('registration/', views.registerPage, name="registration"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)