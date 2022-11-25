from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from uuid import uuid4
from django.conf import settings
from django.urls import reverse
from django_resized import ResizedImageField

import os
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    addressLine1 = models.CharField(null=True,blank=True,max_length=200)
    addressLine2 = models.CharField(null=True,blank=True,max_length=200)
    city = models.CharField(null=True,blank=True,max_length=200)
    province = models.CharField(null=True,blank=True,max_length=200)
    country = models.CharField(null=True,blank=True,max_length=200)
    postalCode = models.CharField(null=True,blank=True,max_length=200)
    profileimage = ResizedImageField(size=[200,200], quality=90, upload_to='profile_images')
    
    #utility variables
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return  '{} {} {}'.format(self.user.first_name, self.user.last_name, self.user.email)

    
         

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]


        self.slug = slugify('{} {} {}'.format( self.user.first_name, self.user.last_name, self.user.email))
        self.last_updated = timezone.localtime(timezone.now())
        super(Profile, self).save(*args, **kwargs)




class Blog(models.Model):
    title = models.CharField(max_length=200)
    blogIdea  = models.CharField(null=True,blank=True,max_length=200)
    keywords = models.CharField(null=True,blank=True,max_length=300)
    audience = models.CharField(null=True,blank=True,max_length=100)
    wordCount = models.CharField(null=True,blank=True,max_length=100)


    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)


    #utility variables
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return  '{} {}'.format(self.title, self.uniqueId)

    
         

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]


        self.slug = slugify('{} {}'.format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        super(Blog, self).save(*args, **kwargs)



class BlogSection(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(null=True,blank=True)
    wordCount = models.CharField(null=True,blank=True,max_length=200)
    
    
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)


    #utility variables
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return  '{} {}'.format(self.title, self.uniqueId)

    
         

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]


        self.slug = slugify('{} {}'.format(self.title, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())
        #count words
        if self.body:
            x = len(self.body.split(' '))
            self.wordCount = str(x)
        super(BlogSection, self).save(*args, **kwargs)