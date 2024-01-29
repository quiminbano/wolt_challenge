from django.http import JsonResponse

def	index(request):
	return JsonResponse({'error': 'Bad request'}, status=400)