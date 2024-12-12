
# Create your models here.

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField


class CustomUserManager(BaseUserManager):
    def create_user(self,email, full_name, password=None,**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,full_name,password,**extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('learner','Learner'),
        ('educator','Educator'),
    )
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=250)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return f'{self.full_name} - {self.email} - {self.user_type}'


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class LearnerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Interest, blank=True)
    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    # profile_image = models.ImageField(upload_to='profile_images', default='profile_images/profile.webp')
    # banner_image = models.ImageField(upload_to='banner_images', default='banner_images/banner.webp')
    # profile_image = CloudinaryField('profile_image', default='profile_images/profile.webp')
    # banner_image = CloudinaryField('banner_image', default='banner_images/banner.webp')
    profile_image = CloudinaryField('profile_image',
                                    default='https://res.cloudinary.com/dzchm8yml/image/upload/v1726752664/yjavnsy8nu8xiqvqeeov.jpg')
    banner_image = CloudinaryField('banner_image',
                                   default='https://res.cloudinary.com/dzchm8yml/image/upload/v1726758796/cmlwhcdl4unrdcipflrv.webp')

    # new fields
    github_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    best_describe = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return f"{self.user}"


class EducatorProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, blank=True)
    qualification = models.CharField(max_length=255,blank=True)
    experience = models.IntegerField(null=True,blank=True)
    github_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    # profile_image = models.ImageField(upload_to='profile_images', default='profile_images/profile.webp')
    # banner_image = models.ImageField(upload_to='banner_images', default='banner_images/banner.webp')

    profile_image = CloudinaryField('profile_image', default='https://res.cloudinary.com/dzchm8yml/image/upload/v1726752664/yjavnsy8nu8xiqvqeeov.jpg')
    banner_image = CloudinaryField('banner_image', default='https://res.cloudinary.com/dzchm8yml/image/upload/v1726758796/cmlwhcdl4unrdcipflrv.webp')

#     new fields
    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    best_describe = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.full_name}"

