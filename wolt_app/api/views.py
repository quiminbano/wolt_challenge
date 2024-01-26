from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def	isValidKeys(decodedBody):
	validWords = ['cart_value', 'delivery_distance', 'number_of_items', 'time']
	for key in decodedBody:
		if not key in validWords:
			return False
	return True

@csrf_exempt #Removed the csrf protection to be able to send request through postman or thunderclient
def	receiveRequest(request):
	if (request.method != 'POST'):
		return JsonResponse({'success': False, 'error': 'Bad request'}, status=400)
	if (request.headers.get('Content-Type') != 'application/json'):
		return JsonResponse({'success': False, 'error': 'Invalid format for content'}, status=400)
	try:
		decodedBody = json.loads(request.body.decode())
	except json.JSONDecodeError:
		return JsonResponse({'success': False, 'error': 'Invalid format for content of the body'}, status=400)
	if not isValidKeys(decodedBody):
		return JsonResponse({'success': False, 'error': 'Invalid format for content of the body'}, status=400)
	return JsonResponse({'success': True, 'error': 'Invalid format for content of the body'}, status=200)
