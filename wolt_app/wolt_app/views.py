from django.http import JsonResponse

def	index(request):
	return JsonResponse({'success': False, 'error': 'Bad request'}, status=400)