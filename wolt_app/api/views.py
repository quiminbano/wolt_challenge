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
			self.__deliveryFee = self.__calculateDeliveryFee()
		except (json.JSONDecodeError, JSONInputError, OverflowError):
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
		except (KeyError, OverflowError):
			raise JSONInputError

	def	__isValidType(self):
		integersList = [self.__cartValue, self.__deliveryDistance, self.__numberOfItems]
		for integers in integersList:
			if (str(type(integers)) != "<class 'int'>") or (integers < 0):
				raise JSONInputError
		if ((str(type(self.__time)) != "<class 'str'>") or (re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', self.__time) == None)):
			raise JSONInputError
		try:
			self.__timeObject = parser.parse(self.__time)
			timeInEpoch = self.__timeObject.timestamp()
			if ((timeInEpoch > time.time()) or (timeInEpoch < float(1412542800))): # 1412542800 = October 6th of 2014 00:00 in Helsinki Time
				raise JSONInputError
		except (parser.ParserError, OverflowError, JSONInputError):
			raise JSONInputError

	def	__calculateDeliveryFee(self):
		result = 0
		if self.__cartValue >= 20000:
			return result
		try:
			for i in range(1, 4):
				match i:
					case 1:
						result = result + self.__feeFromCartValue()
					case 2:
						result = result + self.__feeFromDeliveryDistance()
					case _:
						result = result + self.__feeFromNumberOfItems()
				if result >= 1500:
					break
			if self.__timeObject.weekday() == 5 and (self.__timeObject.hour >= 15 and self.__timeObject.hour <= 19):
				result = round(float(result) * 1.2)
		except OverflowError:
			raise JSONInputError
		if result >= 1500:
			result = 1500
		return result

	def	__feeFromCartValue(self):
		result = 0
	
		if self.__cartValue < 1000:
			result = 1000 - self.__cartValue
		return result

	def	__feeFromDeliveryDistance(self):
		result = 200
		if self.__deliveryDistance <= 1000:
			return result
		for i in range(1001, (self.__deliveryDistance + 1), 500):
			result = result + 100
		return result

	def	__feeFromNumberOfItems(self):
		result = 0
		if self.__numberOfItems <= 4:
			return result
		for i in range(5, (self.__numberOfItems + 1)):
			result = result + 50
		if self.__numberOfItems > 12:
			result = result + 120
		return result

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
	result = requestHandled.getDeliveryFee()
	return JsonResponse({'success': True, 'delivery_fee': result}, status=200)