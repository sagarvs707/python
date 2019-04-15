from django.conf.urls import url
from .views import  CourseDetail, course_post, mentors_details, youtube_list, Mentors_Update,youtubedetail
from django.urls import path

urlpatterns = [
    path('coursepost/',course_post),
    url(r'^get/(?P<id>\d+)/$', CourseDetail.as_view()),
    url(r'^delete/(?P<id>\d+)/$', CourseDetail.as_view()),
    url(r'^put/(?P<id>\d+)/$', CourseDetail.as_view()),


    path('mentors/', mentors_details),
    url(r'^get_mentors/(?P<id>\d+)/$', Mentors_Update.as_view()),
    url(r'^delete_mentors/(?P<id>\d+)/$', Mentors_Update.as_view()),
    url(r'^update_mentors/(?P<id>\d+)/$', Mentors_Update.as_view()),

    path('youtube/', youtube_list),
    url(r'^get_youtube/(?P<id>\d+)/$', youtubedetail.as_view()),
    url(r'^delete_youtube/(?P<id>\d+)/$', youtubedetail.as_view()),
    url(r'^put_youtube/(?P<id>\d+)/$', youtubedetail.as_view()),

]

