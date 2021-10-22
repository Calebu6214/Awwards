from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = CloudinaryField('profile_pics/', blank=True, default = 'https://www.kindpng.com/picc/m/78-785827_user-profile-avatar-login-account-male-user-icon.png')

    def __str__(self):
        return self.user.username

    

    def save_profile(self):
        self.save()                   

    def delete_profile(self):
        self.delete()
    
    
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
        if created:
                    Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
