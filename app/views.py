# views.py
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *


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


