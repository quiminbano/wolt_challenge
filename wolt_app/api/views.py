from datetime import datetime
from dateutil import parser
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json

class JSONInputError(Exception):
	pass

class handleRequest():

	def __isValidType(self):
		integersList = [self.__cartValue, self.__deliveryDistance, self.__numberOfItems]
		for integers in integersList:
			if type(integers).__str__() != "<class 'int'>":
				raise JSONInputError
		if type(self.__time).__str__() != "<class 'str'>":
			raise JSONInputError

	def __isValidKeys(self):
		validWords = ['cart_value', 'delivery_distance', 'number_of_items', 'time']
		for key in self.__decodedBody:
			if not key in validWords:
				raise JSONInputError
		try:
			self.__cartValue = self.__decodedBody['cart_value']
			self.__deliveryDistance = self.__decodedBody['delivery_distance']
			self.__numberOfItems = self.__decodedBody['number_of_items']
			self.__time = self.__decodedBody['time']
		except KeyError:
			raise JSONInputError

	def __init__(self, request : HttpRequest):
		self.__rawImput = ""
		self.__decodedBody = {}
		self.__cartValue = 0
		self.__deliveryDistance = 0
		self.__numberOfItems = 0
		self.__time = ""
		if request.headers.get('Content-Type') != 'application/json':
			raise JSONInputError
		self.__rawImput = request.body.decode()
		try:
			self.__decodedBody = json.loads(self.__rawImput)
			self.__isValidKeys()
			self.__isValidType()
		except (json.JSONDecodeError, JSONInputError):
			raise JSONInputError
	
	def __str__(self):
		return "handleRequestClass"
	

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
