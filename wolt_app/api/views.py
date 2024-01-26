from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt #Removed the csrf protection to be able to send request through postman or thunderclient
def	receiveRequest(request):
	match request.method:
		case 'GET':
			return JsonResponse({'success': False, 'error': 'Bad request'}, status=400)
		case 'POST':
			return JsonResponse({'success': True, 'message': 'Te amo mi Ossi'}, status=200)
