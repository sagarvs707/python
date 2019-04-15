from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from rest_framework.utils import json


class Course(models.Model):
    course_name = models.CharField(max_length=512,null=True, blank=True)
    course_duration = models.CharField(max_length=512,null=True,blank=True)
    course_contents = models.TextField(max_length=512,null=True,blank=True)
    course_cost = models.FloatField(default=0, null=True)
    modefied_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download_link =models.FileField(null=True,blank=True)

     # def get_data(self):
     #     return json.loads(self.data)

class Mentors(models.Model):
    name = models.CharField(max_length=512,null=False,blank=False)
    discription = models.CharField(max_length=512,null=True,blank=True)
    photo = models.CharField(max_length=512,null=True)

class Youtubeplayerlist(models.Model):
    name = models.CharField(max_length=512,null=True,blank=True)
    urls = models.URLField(null=True,blank=True)

