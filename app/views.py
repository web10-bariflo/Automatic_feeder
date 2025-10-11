# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.conf import settings
from django.shortcuts import render
import traceback
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import FeederSetting
from .serializers import FeederSettingSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


MAX_POINT = 3750  # 100% = 3750 points

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("🔵 Received data:", data)

            device_id = data.get('Device_id')
            user_name = data.get('User_name')
            password = data.get('password')
            mob = data.get('Mob')
            email = data.get('Email')

            if not all([device_id, user_name, mob, email]):
                return JsonResponse({'error': 'Device_id, User_name, Mob, and Email are required.'}, status=400)

            if MyUser.objects.filter(Device_id=device_id).exists():
                return JsonResponse({'error': 'Device_id already exists.'}, status=409)

            if MyUser.objects.filter(Mob=mob).exists():
                return JsonResponse({'error': 'Mobile number already registered.'}, status=409)

            if MyUser.objects.filter(Email=email).exists():
                return JsonResponse({'error': 'Email already registered.'}, status=409)

            user = MyUser.objects.create(
                Device_id=device_id,
                User_name=user_name,
                password=password,
                Mob=mob,
                Email=email
            )

            return JsonResponse({
                'message': 'User created successfully.',
                'Device_id': user.Device_id,
                'User_name': user.User_name,
                'Mob': user.Mob,
                'Email': user.Email
            }, status=201)

        except Exception as e:
            print("🔥 Exception:", str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)



@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            identifier = data.get('identifier')
            password = data.get('password')

            if not all([identifier, password]):
                return JsonResponse({'error': 'Username/Email/Mobile and password are required.'}, status=400)

            try:
                # Determine login method
                if identifier.isdigit():
                    user = MyUser.objects.get(Mob=int(identifier))
                elif '@' in identifier:
                    user = MyUser.objects.get(Email=identifier)
                else:
                    user = MyUser.objects.get(User_name=identifier)

                if user.password == password:
                    return JsonResponse({
                        'message': 'Login successful',
                        'Device_id': user.Device_id,
                        'User_name': user.User_name,
                        'Mob': user.Mob,
                        'Email': user.Email
                    }, status=200)
                else:
                    return JsonResponse({'error': 'Invalid password'}, status=401)

            except MyUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'Email is required.'}, status=400)

            try:
                user = MyUser.objects.get(Email=email)
                reset_link = f"http://20.6.88.47:8000/reset-password/?email={user.Email}"

                from django.core.mail import send_mail
                send_mail(
                    subject="Reset Your Password",
                    message=f"Hi {user.User_name},\n\nClick the link to reset your password:\n{reset_link}",
                    from_email="care.bariflolabs@gmail.com",
                    recipient_list=[user.Email],
                    html_message=f"""
                        <p>Hi {user.User_name},</p>
                        <p>Click the link below to reset your password:</p>
                        <p><a href="{reset_link}">{reset_link}</a></p>
                        <p>If you did not request this, please ignore this email.</p>
                    """,
                    fail_silently=False,
                )



                return JsonResponse({'message': 'Reset link sent to your email.'}, status=200)

            except MyUser.DoesNotExist:
                return JsonResponse({'error': 'Email not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            new_password = data.get('new_password')

            if not all([email, new_password]):
                return JsonResponse({'error': 'Email and new password are required.'}, status=400)

            try:
                user = MyUser.objects.get(Email=email)
                user.password = new_password
                user.save()
                return JsonResponse({'message': 'Password updated successfully.'}, status=200)

            except MyUser.DoesNotExist:
                return JsonResponse({'error': 'User with this email not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)




@csrf_exempt
def reset_password_page(request):
    email = request.GET.get('email', '')
    return render(request, 'reset_password.html', {'email': email})




@csrf_exempt
def auto_feeder_data_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not isinstance(data, list):
                data = [data]

            saved_items = []

            for item in data:
                auto_start_time = item.get('auto_start_time')
                auto_end_time = item.get('auto_end_time')
                auto_feed_rate = item.get('auto_feed_rate')
                auto_sprinkle_rate = item.get('auto_sprinkle_rate')

                if not all([auto_start_time, auto_end_time, auto_feed_rate, auto_sprinkle_rate]):
                    return JsonResponse({'error': 'All fields are required for each item'}, status=400)

                feeder = AutoFeederData.objects.create(
                    auto_start_time=auto_start_time,
                    auto_end_time=auto_end_time,
                    auto_feed_rate=auto_feed_rate,
                    auto_sprinkle_rate=auto_sprinkle_rate
                )

                saved_items.append({
                    'id': feeder.id,
                    'auto_start_time': feeder.auto_start_time,
                    'auto_end_time': feeder.auto_end_time,
                    'auto_feed_rate': feeder.auto_feed_rate,
                    'auto_sprinkle_rate': feeder.auto_sprinkle_rate,
                    'timestamp': feeder.Timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # or .isoformat()
                })

            return JsonResponse({
                'message': 'Auto Feeder data saved successfully',
                'data': saved_items
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


@csrf_exempt
def get_auto_feeder_data(request):
    if request.method == 'GET':
        data = AutoFeederData.objects.all().order_by('-Timestamp')[:50].values(
            'id', 
            'auto_start_time', 
            'auto_end_time', 
            'auto_feed_rate', 
            'auto_sprinkle_rate'
        )
        return JsonResponse(list(data), safe=False, status=200)
    
    return JsonResponse({'error': 'Only GET method is allowed'}, status=405)





@csrf_exempt
def manual_feeder_data_post(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not isinstance(data, list):
                return JsonResponse({'error': 'Expected a list of data entries'}, status=400)

            created_entries = []

            for item in data:
                manual_start_time = item.get('manual_start_time')
                manual_end_time = item.get('manual_end_time')
                manual_feed_rate = item.get('manual_feed_rate')
                manual_sprinkle_rate = item.get('manual_sprinkle_rate')

                # Validate individual entry
                if not all([manual_start_time, manual_end_time, manual_feed_rate, manual_sprinkle_rate]):
                    return JsonResponse({'error': 'All fields are required for each entry'}, status=400)

                feeder = ManualFeederData.objects.create(
                    manual_start_time=manual_start_time,
                    manual_end_time=manual_end_time,
                    manual_feed_rate=manual_feed_rate,
                    manual_sprinkle_rate=manual_sprinkle_rate
                )

                created_entries.append({
                    'id': feeder.id,
                    'manual_start_time': feeder.manual_start_time,
                    'manual_end_time': feeder.manual_end_time,
                    'manual_feed_rate': feeder.manual_feed_rate,
                    'manual_sprinkle_rate': feeder.manual_sprinkle_rate,
                    'timestamp': feeder.Timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # Or use .isoformat()
                })

            return JsonResponse({
                'message': 'Manual feeder data saved successfully',
                'data': created_entries
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)



@csrf_exempt
def get_manual_feeder_data(request):
    if request.method == 'GET':
        data = ManualFeederData.objects.all().order_by('-Timestamp')[:50].values(
            'id',
            'manual_start_time',
            'manual_end_time',
            'manual_feed_rate',
            'manual_sprinkle_rate'
        )
        return JsonResponse(list(data), safe=False, status=200)

    return JsonResponse({'error': 'Only GET method is allowed'}, status=405)



def latest_alerts(request):
    latest_alerts = Alert_message.objects.order_by('-Timestamp')[:5]
    data = [{'alert': a.alert, 'timestamp': a.Timestamp} for a in latest_alerts]
    return JsonResponse(data, safe=False)




@csrf_exempt
@require_http_methods(["GET", "POST"])
def feeder_settings(request):
    if request.method == 'GET':
        settings = FeederSetting.objects.all().order_by('-created_at')
        serializer = FeederSettingSerializer(settings, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            percentage = data.get('percentage')

            try:
                percentage = float(percentage)
                if percentage < 0 or percentage > 100:
                    return JsonResponse(
                        {"error": "Percentage must be between 0 and 100"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except (ValueError, TypeError):
                return JsonResponse(
                    {"error": "Percentage must be a valid number"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            point_value = (percentage / 100) * MAX_POINT

            setting = FeederSetting(percentage=percentage, point_value=point_value)
            setting.save()

            serializer = FeederSettingSerializer(setting)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=status.HTTP_400_BAD_REQUEST
            )
            

@require_http_methods(["GET"])
def predefined_percentages(request):
    predefined_data = []
    
    # Generate percentages from 10 to 100 with step of 10
    for percentage in range(10, 101, 10):
        point_value = int((percentage / 100) * 3750)
        
        predefined_data.append({
            "id": percentage // 10,  # Generate IDs 1, 2, 3, ..., 10
            "percentage": percentage,
            "point_value": point_value,
            "description": f"{percentage}% = {point_value} points"
        })
    
    return JsonResponse(predefined_data, safe=False)



# @api_view(['GET', 'POST'])
# def feeder_settings(request):
#     if request.method == 'GET':
#         settings = FeederSetting.objects.all().order_by('-created_at')
#         serializer = FeederSettingSerializer(settings, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = FeederSettingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)