# Generated by Django 3.2.8 on 2021-10-23 10:01

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(max_length=255)),
                ('project_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='images')),
                ('project_description', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('link', models.URLField()),
                ('country', django_countries.fields.CountryField(default='Kenya', max_length=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('photo', cloudinary.models.CloudinaryField(blank=True, default='https://www.kindpng.com/picc/m/78-785827_user-profile-avatar-login-account-male-user-icon.png', max_length=255, verbose_name='profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
