from datetime import datetime
from dateutil import parser
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import re
import time

class JSONInputError(Exception):
	pass

class handleRequest():

	def __init__(self, request : HttpRequest):
		self.__rawImput = ""
		self.__decodedBody = {}
		self.__cartValue = 0
		self.__deliveryDistance = 0
		self.__numberOfItems = 0
		self.__time = ""
		self.__deliveryFee = 0
		if request.headers.get('Content-Type') != 'application/json':
			raise JSONInputError
		self.__rawImput = request.body.decode()
		try:
			self.__decodedBody = json.loads(self.__rawImput)
			self.__isValidKeys()
			self.__isValidType()
		except (json.JSONDecodeError, JSONInputError):
			raise JSONInputError
		self.__deliveryFee = self.__calculateDeliveryFee()

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

	def	__isValidType(self):
		integersList = [self.__cartValue, self.__deliveryDistance, self.__numberOfItems]
		for integers in integersList:
			if (type(integers).__str__() != "<class 'int'>") or (integers < 0):
				raise JSONInputError
		if ((type(self.__time).__str__() != "<class 'str'>") or (re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', self.__time) == None)):
			raise JSONInputError
		try:
			self.__timeObject = parser.parse(self.__time)
			timeInEpoch = self.__timeObject.timestamp()
			if ((timeInEpoch > time.time()) or (timeInEpoch < float(1412542800))): # 1412542800 = October 6th of 2014 00:00 in Helsinki Time
				raise JSONInputError
		except (parser.ParserError, OverflowError, JSONInputError):
			raise JSONInputError

	def	__calculateDeliveryFee(self):
		if self.__cartValue >= 20000:
			return 0

	def	getDeliveryFee(self):
		return self.__deliveryFee

	def	__str__(self):
		return "handleRequestClass"
	

@csrf_exempt #Removed the csrf protection to be able to send request through postman or thunderclient
def	receiveRequest(request):
	if (request.method != 'POST'):
		return JsonResponse({'success': False, 'error': 'Bad request'}, status=400)
	try:
		requestHandled = handleRequest(request=request)
	except JSONInputError:
		return JsonResponse({'success': False, 'error': 'Invalid format of the request'}, status=400)