from django.shortcuts import redirect
from rest_framework.views import APIView
from .serializers import SignupSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import jwt

from .models import Signup
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
import http.client


@csrf_exempt
@api_view(['POST'])
def register_view(request):
    try:
        if request.method == 'POST':
            email = request.data.get('email')
            full_name = request.data.get('full_name')
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')
            community = request.data.get('community')

            try:
                validate = Signup.objects.get(email=email)
                if validate is not None:
                    return Response({'status':'error', 'code':'400', 'message':'Email Id is already Exists'})

            except Exception as e:
                url = "/api/sendotp.php?authkey=273205Ax8ophJB65cbaae80&message=your verification code is %23%23OTP%23%23&sender=611332&mobile=+91"
                conn = http.client.HTTPConnection("control.msg91.com")
                conn.request("POST", url + str(phone_number))
                res = conn.getresponse()
                data = res.read()
                data_respond = data.decode("utf-8")
                message1 = json.loads(data_respond)
                message = message1['message']

                form = ImageUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    try:
                        model_pic = request.FILES['profile_picture']
                        fs = FileSystemStorage()
                        filename = fs.save(model_pic.name, model_pic)
                        uploaded_file_url = filename
                    except:
                        uploaded_file_url = request.data.get('profile_picture')
                payload = {
                    'email': email,
                    'full_name': full_name,
                    'phone_number': phone_number,
                    'password': password,
                    'community': community,
                    # 'sessionid': str(message),
                    'profile_picture':str(uploaded_file_url),
                }

                token = jwt.encode(payload, 'secret', algorithm='HS256')
                return Response({'status': 'success', 'statuscode': '200', 'message': 'token generated successfully, OTP sent to your given number', 'token': token})
        else:
            return Response({'status': 'failed', 'statuscode':'400', 'message': 'failed to generate token!'})
    except Exception as e:
        return Response({'status': e, 'statuscode':'400', 'message': 'EmailId is already exists!'})



@csrf_exempt
@api_view(['POST'])
def validate_registration_otp(request):
    if request.method == 'POST':
        get_otp = request.data.get('otp')
        get_token = request.data.get('token')
        phone = request.data.get('phone_number')


        token1 = jwt.decode(get_token, 'secret', algorithms=['HS256'])
        messageid = token1.get("sessionid")

        url = "/api/verifyRequestOTP.php?authkey=273205Ax8ophJB65cbaae80&mobile=+91" + phone + "&otp="
        print(url)

        conn = http.client.HTTPSConnection("control.msg91.com")

        payload = messageid
        headers = {'content-type': "application/x-www-form-urlencoded"}

        conn.request("POST", url + get_otp, payload, headers)
        res = conn.getresponse()
        data = res.read()
        verified = data.decode("utf-8")
        y = json.loads(verified)
        Status = y['type']
        msg_status = y['message']

        try:
            if Status == 'success':
                data = token1.copy()
                payload = {
                    'email': data.get("email"),
                    'full_name': data.get("full_name"),
                    'phone_number': data.get("phone_number"),
                    'password': data.get("password"),
                    'profile_picture':data.get("profile_picture"),
                    'community': data.get("community")
                }
                reg = Signup(**payload)
                reg.save()
                return Response({'status': 'Success', 'status_code': '200', 'message': 'Registered Successfully'})
            elif msg_status == 'already_verified':
                return Response({'status': 'error', 'status_code': '400', 'message': 'OTP already sent'})
            elif Status == 'error':
                return Response({'status': 'error', 'status_code': '400', 'message': 'maximum attempt'})

        except Exception as e:
            return Response({'status': 'error', 'statuscode': '400', 'Message': 'OTP matching failed'})
    else:
        return Response({'status': 'error', 'statuscode': '400', 'Message': 'OTP matching failed'})


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
            return Response({'status':str(e), 'statuscode':'400', 'message':'User doesnot exist'})


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
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'password': user.password,
                'profile_picture': 'Profil_pictur/' + str(user.profile_picture),
                'community': user.community,
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
        user_id = request.data.get('user_id')
        current_password = request.data.get('password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')
        try:
            user = Signup.objects.get(id=user_id)
            if user.password == current_password:
                try:
                    user.password = new_password1
                    user.save()
                    return Response({'status':'success', 'statuscode':'200', 'message':'Password is reset successfully'})
                except Exception as e:
                    return Response({'status':'error', 'statuscode':'400', 'message':'old password is invalide'})
            else:
                return Response({'status':'error', 'statuscode':'400', 'message':'Password are does not matching'})
        except Exception as e:
            return Response({'status': 'error', 'code': '400', 'message': 'Invalid credential'})


@csrf_exempt
@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        conf_password = request.data.get('conf_password')

        try:
            if new_password == conf_password:
                get_data = Signup.objects.get(email=email)
                phone_number = get_data.phone_number

                url = "/api/sendotp.php?authkey=273205Ax8ophJB65cbaae80&message=your verification code is %23%23OTP%23%23&sender=611332&mobile=+91"
                conn = http.client.HTTPConnection("control.msg91.com")
                conn.request("POST", url + str(phone_number))
                res = conn.getresponse()
                data = res.read()
                data_respond = data.decode("utf-8")
                message1 = json.loads(data_respond)
                message = message1['message']

                mail = get_data.email
                phone = get_data.phone_number

                payload = {
                    'email': mail,
                    'phone_number': phone,
                    'session_id': str(message),
                    'new_password': new_password,
                    'conf_password': conf_password,
                    'sessionid': str(message),

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
            phone = request.data.get('phone_number')

            token1 = jwt.decode(get_token, 'secret', algorithms=['HS256'])
            messageid = token1.get("session_id")

            url = "/api/verifyRequestOTP.php?authkey=273205Ax8ophJB65cbaae80&mobile=+91" + phone + "&otp="
            conn = http.client.HTTPSConnection("control.msg91.com")

            payload = messageid
            headers = {'content-type': "application/x-www-form-urlencoded"}

            conn.request("POST", url + get_otp, payload, headers)
            res = conn.getresponse()
            data = res.read()
            verified = data.decode("utf-8")
            y = json.loads(verified)
            Status = y['type']
            msg_status = y['message']

            try:
                if Status == 'success':
                    email = token1.get("email")
                    new_password = token1.get("new_password")
                    conf_password = token1.get("conf_password")

                    get_data = Signup.objects.get(email=email)
                    get_data.password = new_password
                    get_data.save()
                    return Response({'status': 'success', 'statuscode': '200', 'message': 'Password is changed successfully'})
                elif msg_status == 'already_verified':
                    return Response({'status': 'error', 'status_code': '400', 'message': 'OTP already sent'})
                elif Status == 'error':
                    return Response({'status': 'error', 'status_code': '400', 'message': 'maximum attempt'})

            except Exception as e:
                return Response({'status':'error', 'code':'404', 'Message': str(e)})

    except Exception as e:
        return Response({'status': 'error', 'code': '404', 'Message': str(e)})

@api_view(['POST'])
def push_notification(request):
    if request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')

        payload = {
            'title':title,
            'description':description,
        }

        push_notify(title, description)

    return Response({'status':'success'})

def push_notify(title, description):
    from pusher_push_notifications import PushNotifications

    beams_client = PushNotifications(
        instance_id='e963a157-8815-48fa-8daa-256a18458374',
        secret_key='D1AD8E16FBFD113A9CFD1760501B740E41F9A86FF893B7019411F620756A44CE',
    )

    response = beams_client.publish_to_interests(
        interests=['hello'],
        publish_body={'apns': {'aps': {'alert': 'Viyaan Notification'}}, 'fcm': {'notification': {'title': str(title), 'body': 'Description' +str(description)} } } )

    print(response['publishId'])

