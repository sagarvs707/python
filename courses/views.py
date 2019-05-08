from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Mentors, Youtubeplayerlist
from .serializers import CourseSerializer, MentorsSerializer,YoutubeplayerlistSerializer
from .models import Course
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404

@csrf_exempt
@api_view(['POST'])
def course_post(request):
    try:
        if request.method == 'POST':
            cname = request.data.get('courname')
            cdur = request.data.get('courduration')
            ccc = request.data.get('courcontents')
            ccost = request.data.get('coursecost')
            payload = {
                'course_name':cname,
                'course_duration':cdur,
                'course_contents':ccc,
                'course_cost':ccost,
            }
            r = Course(**payload)
            r.save()
            return Response({'status':'success', 'statuscode':'200', 'message':'saved successfully'})
        else:
            return Response({'status':'Fail', 'statuscode':'400', 'message':'course list does not posted'})

    except Exception as e:
            return Response({'status':'Fail', 'statuscode':'400', 'message':'course list does not posted'})


class CourseDetail(APIView):
    def get_object(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, id):
        try:
            course = self.get_object(id)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Exception as e:
            return Response({'status':'Fail', 'statuscode':'400', 'message':'course not found'})

    def delete(self,request,id):
        try:
            course = self.get_object(id)
            course.delete()
            return Response({'status':'success','statuscode':'204','messsage':'coursedeleted successfully'})
        except Exception as e:
            return Response({'status':'fail','statuscode':'400','messsage':'course not found'})

    def put(self, request, id,):
        update = self.get_object(id)
        serializer = CourseSerializer(update, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'status':'success','statuscode':'204','message':'Data updatefailed'})
        except Exception as e:
            return Response({'status':'success','statuscode':'204','message':'invalid data'})

@csrf_exempt
@api_view(['GET'])
def view_all_courses(request):
    if request.method == 'GET':
        view_all = Course.objects.all()
        view_list = []
        for view in view_all:
            payload = {
                'id': view.id,
                'course_name': view.course_name,
                'course_duration': view.course_duration,
                'course_contents': view.course_contents,
                'course_cost': view.course_cost,
            }
            view_list.append(payload)
        return JsonResponse({'status': 'success', 'code': '200', 'all_courses': view_list})
    else:
        return Response({'status': 'fail', 'code': '404', 'message': 'Inavalid cradentials'})


@csrf_exempt
@api_view(['GET','POST','PUT'])
def mentors_details(request):
    if request.method == 'POST':
        try:
            mname = request.data.get('mentorname')
            mdiscription =request.data.get('mendiscription')
            photo = request.data.get('photo')
            payload ={
                'name':mname,
                'discription':mdiscription,
                'photo':photo
            }
            m = Mentors(**payload)
            m.save()
            return Response({'status':'ok', 'statuscode':'200', 'message':'mentors added sucesfully'})
        except Exception as e:
            return Response({'status':'Fail', 'statuscode':'400', 'message':'mentor doesnot exists'})

class Mentors_Update(APIView):
    def get_object(self, id):
        try:
            return Mentors.objects.get(id=id)
        except Mentors.DoesNotExist:
            raise Http404

    def get(self, request, id):
        try:
            mentors = self.get_object(id=id)
            serializer = MentorsSerializer(mentors)
            return Response(serializer.data)
        except Exception as e:
            return  Response({'status':'Fail', 'statuscode':'400', 'message':'mentor doesnot exists'})
    def delete(self,request,id):
        try:
            mentors = self.get_object(id)
            mentors.delete()
            return Response({'status':'succes', 'statuscode':'200', 'message':'mentor deleted sucessfully'})
        except Exception as e:
            return Response({'status':'Fail', 'statuscode':'400', 'message':'mentor doesnot exists'})

    def put(self, request, id, format=None):
        try:
            update = self.get_object(id)
            serializer = MentorsSerializer(update, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Exception as e:
            return Response({'status':'Fail', 'statuscode':'400', 'message':'mentorsupdated sucesfully'})

@api_view(['POST'])
def youtube_list(request):
    if request.method == 'POST':
        name = request.data.get('name')
        url = request.data.get('url')
        context ={
            'name':name,
            'urls':url
        }
        y = Youtubeplayerlist(**context)
        y.save()
        return Response({'status':'ok', 'code':'200', 'message':'list added sucesfully'})

class youtubedetail(APIView):
    def get_object(self, id):
        try:
            return Youtubeplayerlist.objects.get(id=id)
        except Youtubeplayerlist.DoesNotExist:
            raise Http404

    def get(self, request, id):
        try:
            Youtubeplayerlist= self.get_object(id)
            serializer = YoutubeplayerlistSerializer(Youtubeplayerlist)
            return Response(serializer.data)
        except Exception as e:
            return Response({'status':'FAil', 'code':'400', 'message':'not found'})

    def delete(self,request,id):
        try:
            Youtubeplayerlist = self.get_object(id)
            Youtubeplayerlist.delete()
            return Response({'status':'ok', 'code':'200', 'message':'vedio deleted sucesfully'})
        except Exception as e:
            return Response({'status':'Fail', 'code':'400', 'message':'vedio not found'})

    def put(self, request, id,):
        update = self.get_object(id)
        serializer = YoutubeplayerlistSerializer(update, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'ok', 'code':'200', 'message':'updated sucesfully'})
            else:
                return Response({'status':'error', 'code':'404', 'message':'update failed'})

        except:
             return Response({'status':'Fail', 'code':'400', 'message':'vedio not foound'})