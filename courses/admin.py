from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course,Mentors,Youtubeplayerlist
# Register your models here.


admin.site.register(Course)
admin.site.register(Mentors)
admin.site.register(Youtubeplayerlist)