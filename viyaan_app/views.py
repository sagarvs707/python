from django.shortcuts import redirect
from rest_framework.views import APIView
from .serializers import SignupSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import jwt

from django.core.files.storage import FileSystemStorage
from .models import Document, Signup
from .forms import DocumentForm



@csrf_exempt
@api_view(['POST'])
def register_view(request):
    try:
        if request.method == 'POST':
            email = request.data.get('email')
            full_name = request.data.get('full_name')
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')

            session_otp = requests.post('https://2factor.in/API/V1/26bd58b6-5841-11e9-a6e1-0200cd936042/SMS/+91'+phone_number+'/AUTOGEN', params=request.POST)
            session = session_otp.content
            session1 = session.decode("utf-8")
            x = json.loads(session1)
            session_id = x['Details']

            payload = {
                'email': email,
                'full_name': full_name,
                'phone_number': phone_number,
                'password': password,
                'sessionid': str(session_id)
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')
            return Response({'status': 'success', 'statuscode': '200', 'message': 'token generated successfully, OTP sent to your given number', 'token': token})

        return Response({'status': 'failed', 'statuscode':'400', 'message': 'failed to generate token!'})

    except Exception as e:
        return Response({'status': e, 'statuscode':'400', 'message': 'EmailId is already exists!'})



@csrf_exempt
@api_view(['GET','POST'])
def validate_registration_otp(request):
    try:
        if request.method == 'POST':
            get_otp = request.data.get('otp')
            get_token = request.data.get('token')

            token1 = jwt.decode(get_token, 'secret', algorithms=['HS256'])
            x = token1.get("sessionid")

            verified = requests.post('https://2factor.in/API/V1/26bd58b6-5841-11e9-a6e1-0200cd936042/SMS/VERIFY/'+x+'/'+str(get_otp), params=request.POST)

            a = verified.content
            session_otp = a.decode("utf-8")
            y = json.loads(session_otp)
            Status = y['Status']

            try:
                if Status == 'Success':
                    data = token1.copy()
                    payload = {
                        'email': data.get("email"),
                        'full_name': data.get("full_name"),
                        'phone_number': data.get("phone_number"),
                        'password': data.get("password"),
                    }
                    reg = Signup(**payload)
                    reg.save()
                    return Response({'status':'Success', 'status_code': '200', 'message': 'Registered Successfully'})
                else:
                    return Response({'status': 'error', 'statuscode':'400', 'Message':'OTP matching failed'} )
            except Exception as e:
                return Response(str(e))

    except Exception as e:
        return Response({'status': str(e), 'statuscode':'400', 'message': 'Invalid OTP'})


class SignupDelete(APIView):

    def get_object(self, id):
        try:
            return Signup.objects.get(id=id)
        except Exception as e:
            return Response({'status': 'error', 'statuscode':'404', 'Message':'detile not found'})
            # Signup.DoesNotExist:
            # raise Http404

    def get(self, request, id):
        try:
            if id is not None:
                user = self.get_object(id)
                serializer = SignupSerializer(user)
                return Response(serializer.data)
            else:
                return Response({'status': 'error', 'statuscode':'404', 'Message':'Id not found'})
        except Exception as e:
            return Response({'status': 'error', 'statuscode':'404', 'Message':'Id not found'})

    def put(self, request, id, format=None):
        update = self.get_object(id)
        serializer = SignupSerializer(update, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'status':'success', 'statuscode':'200', 'message':'Updated successfully'})
            return Response(serializer.errors,)
        except Exception as e:
            return Response({'status': str(e), 'statuscode': '404', 'message': 'User doesnot exist'})


    def delete(self, request, id, format=None):
        try:
            deleteuser = self.get_object(id)
            deleteuser.delete()
            return Response({'status': 'success', 'statuscode': '204', 'messages': 'Deleted successfully'})
        except Exception as e:
            return Response({'status':'error', 'statuscode':'400', 'message':'User doesnot exist'})


@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = Signup.objects.get(email=email)
        if user.password == password:
            user.is_active = True
            user.save()
            payload = {
                'id': user.id
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            redirect_url = request.GET.get('next')
            if redirect_url:
                return redirect(redirect_url)
            return Response({'status': 'success', 'statuscode': '200', 'messages': 'Login sccessflly', 'token': token})
        else:
            return Response({'status':'Error', 'statuscode': '400', 'message':'Invalid password'})
    except Exception as e:
        return Response({'status':'Error', 'statuscode':'400', 'message':'Invalid emailId and password! Pleas Enter valid EmailId and Password'})


@api_view(['POST'])
def logout(request):
    try:
        get_token = request.data.get('token')
        token1 = jwt.decode(get_token, 'secret', algorithms=['HS256'])
        x = token1['id']
        # user = Signup.objects.filter(id = x).filter(is_active = True)
        user = Signup.objects.get(id=x)
        if user.is_active == True:
            user.is_active = False
            user.save()
            return Response({'status':'success', 'statuscode': '200', 'message':'Loged out successfully'})
    except Exception as e:
        return Response(str(e))


@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        password = request.data.get('password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')
        if new_password1 == new_password2:
            try:
                user = Signup.objects.get(password=password)
                user.password = new_password1
                user.save()
                return Response({'status':'success', 'statuscode':'200', 'message':'Password is reset successfully'})
            except Exception as e:
                return Response({'status':'error', 'statuscode':'400', 'message':'old password is invalide'})
        else:
            return Response({'status':'error', 'statuscode':'400', 'message':'Password are does not matching'})
    return Response("something went wrong")



@csrf_exempt
@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        conf_password = request.data.get('conf_password')

        try:
            if new_password == conf_password:
                data = Signup.objects.get(email=email)
                session_otp = requests.post('https://2factor.in/API/V1/26bd58b6-5841-11e9-a6e1-0200cd936042/SMS/+91'+data.phone_number+'/AUTOGEN', params=request.POST)

                session = session_otp.content
                session1 = session.decode("utf-8")
                x = json.loads(session1)
                session_id = x['Details']

                data = data.email

                payload = {
                    'data': data,
                    'session_id': session_id,
                    'new_password': new_password,
                    'conf_password': conf_password

                }

                token = jwt.encode(payload, 'secret', algorithm='HS256')

                return Response({'status':'success', 'code':'200', 'Message':'OTP sent to your mobile number', 'token': token})

            else:
                return Response({'status':'error', 'code':'404', 'Message':'Password confirmation failed, password does not matching each other'})
        except Exception as e:
            return Response({'status':'error', 'code':'400', 'Message':'Please enter correct EmailId and Password'})




@api_view(['POST'])
def validate_forgot_password(request):
    try:
        if request.method == 'POST':
            get_otp = request.data.get('otp')
            get_token = request.data.get('token')

            token1 = jwt.decode(get_token, 'secret', algorithms=['HS256'])
            x = token1.get("session_id")

            verified = requests.post('https://2factor.in/API/V1/26bd58b6-5841-11e9-a6e1-0200cd936042/SMS/VERIFY/'+x+'/'+str(get_otp),params=request.POST)

            a = verified.content
            session_otp = a.decode("utf-8")
            y = json.loads(session_otp)
            Status = y['Status']
            try:
                if Status == 'Success':
                    email = token1.get("data")
                    new_password = token1.get("new_password")
                    conf_password = token1.get("conf_password")

                    data = Signup.objects.get(email=email)
                    data.password = new_password
                    data.save()
                    return Response({'status': 'success', 'statuscode': '200', 'message': 'Password is changed successfully'})
                else:
                    return Response({'status':'error', 'code':'404', 'Message':'Invalid OTP'})

            except Exception as e:
                return Response({'status':'error', 'code':'404', 'Message': str(e)})

    except Exception as e:
        return Response({'status':'error', 'code':'404', 'Message':str(e)})


def image_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return Response("success", {'uploaded_pictur': uploaded_file_url})
    return Response("fail")

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return Response("return home page")
    else:
        form = DocumentForm()
    return Response("hello",{'form': form})