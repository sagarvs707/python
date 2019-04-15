from rest_framework import serializers
from .models import Course,Mentors,Youtubeplayerlist


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','course_name','course_duration','course_contents','course_cost')

class MentorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentors
        fields =('id','name','discription','photo')

class YoutubeplayerlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtubeplayerlist
        fields = ('id','name','urls')