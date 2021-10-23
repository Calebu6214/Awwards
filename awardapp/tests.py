from django.test import TestCase
from .models import *

# Create your tests here.
class ProfileTest(TestCase):

    def setUp(self):
        self.user = User(user='kim', bio='yes', photo='kim.png')
        self.user.save()
        self.photo = Profile(photo='kim.png', bio='kim', user=self.new_user)

    def test_instance(self):
        self.assertTrue(isinstance(self.photo, Profile))

    def test_save_method(self):
        self.photo.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)
    
   # Create your tests here.
class ProjectTest(TestCase):

    def setUp(self):
        self.new_user = User(username='kim',bio='yes', photo='kim.png')
        self.new_user.save()
        self.new_project = Profile(project_image='kim.jpg', bio='give', user=self.new_user)
        self.new_project.save()
        self.new_post = Projects(project_title='dust', project_image='tt.jpg', project_description='dust', pub_date='12/12/2021',author='John', link='www.kim.com')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Projects))

    def test_save_post(self):
        self.new_post.save_project()
        post = Projects.objects.all()
        self.assertTrue(len(post)>0)

    

