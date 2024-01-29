from django.test import Client, TestCase
import json

class Tester(TestCase):

	def	initializeTester(self):
		self.client = Client()

	# This method tests the response received from our endpoint when a different request type is sent to our endpoint.
	def	testTypeRequest(self):
		typeList = ['get', 'delete', 'put', 'patch', 'head', 'options']
		for method in typeList:
			if method == 'get':
				response = getattr(self.client, method)('/api/endpoint')
			else:
				response = getattr(self.client, method)('/api/endpoint')
			self.assertEqual(response.status_code, 400)

	# This method test the response received from our endpoint when the number of items changes.
	def	testValidNumberOfItems(self):
		body1 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body2 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 5, "time": "2024-01-15T13:00:00Z"}
		body3 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 12, "time": "2024-01-15T13:00:00Z"}
		body4 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 13, "time": "2024-01-15T13:00:00Z"}
		body5 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 14, "time": "2024-01-19T14:59:00Z"}
		body6 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 20, "time": "2024-01-19T14:59:00Z"}
		listRequest = [body1, body2, body3, body4, body5, body6]
		answers = [710, 760, 1110, 1280, 1330, 1500]
		self.__testLoop(listRequest=listRequest, answers=answers)

	# This method tests the response received from our endpoint when the date changes.
	# This method also tests the differences in the delivery_fee when the date represented is in the rush time and in the normal time.
	def	testValidDates(self):
		body1 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T13:59:00Z"}
		body2 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T14:00:00Z"}
		body3 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T14:59:00Z"}
		body4 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T15:00:00Z"}
		body5 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T18:59:00Z"}
		body6 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T19:00:00Z"}
		body7 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T20:00:00Z"}
		body8 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-18T13:59:00Z"}
		body9 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-18T14:00:00Z"}
		body10 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-18T14:59:00Z"}
		body11 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-18T15:00:00Z"}
		body12 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-18T18:59:00Z"}
		body13 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-18T19:00:00Z"}
		body14 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-18T20:00:00Z"}
		listRequest = [body1, body2, body3, body4, body5, body6, body7, body8, body9, body10, body11, body12, body13, body14]
		answers = [710, 710, 710, 852, 852, 710, 710, 710, 710, 710, 710, 710, 710, 710]
		self.__testLoop(listRequest=listRequest, answers=answers)

	# This method tests the response received from our endpoint when the the delivery_distance is increased.
	def	testValidDeliveryDistance(self):
		body1 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body2 = {"cart_value": 790, "delivery_distance": 2499, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body3 = {"cart_value": 790, "delivery_distance": 2500, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body4 = {"cart_value": 790, "delivery_distance": 2501, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body5 = {"cart_value": 790, "delivery_distance": 2999, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body6 = {"cart_value": 790, "delivery_distance": 3000, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body7 = {"cart_value": 790, "delivery_distance": 3001, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		listRequest = [body1, body2, body3, body4, body5, body6, body7]
		answers = [710, 710, 710, 810, 810, 810, 910]
		self.__testLoop(listRequest=listRequest, answers=answers)

	# This method tests the response received from our endpoint when the cart_value is increased.
	def	testValidCartValue(self):
		body1 = {"cart_value": 590, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body2 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body3 = {"cart_value": 990, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body4 = {"cart_value": 2000, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
		body5 = {"cart_value": 10000, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T14:59:00Z"}
		body6 = {"cart_value": 19999, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T14:59:00Z"}
		body7 = {"cart_value": 20000, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-19T14:59:00Z"}
		listRequest = [body1, body2, body3, body4, body5, body6, body7]
		answers = [910, 710, 510, 500, 500, 500, 0]
		self.__testLoop(listRequest=listRequest, answers=answers)

	# This method let us test different invalid inputs. The details of the test can be found bellow.
	def	testInvalidInputs(self):
		# One field is missing
		body1 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4}
		# There is an extra field.
		body2 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z", "city": 'Helsinki'}
		# One or more than one value are negative
		body3 = {"cart_value": -1000, "delivery_distance": 2235, "number_of_items": -4, "time": "2024-01-15T13:00:00Z"}
		# The Date is in the farer future.
		body4 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "3024-01-15T13:00:00Z"}
		# The Date is before Wolt fundation in Oct 14 of 2014. 00:00 at UTC+2 as reference.
		body5 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 0, "time": "2013-10-24T13:00:00Z"}
		# The number of items is 0
		body6 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 0, "time": "2024-01-15T13:00:00Z"}
		# One or more of the categories is not well written
		body7 = {"cart_valuei": 790, "delivery_distancei": 2235, "number_of_itemsi": 4, "timei": "2024-01-15T13:00:00Z"}
		# The date is in a different format than the specified
		body8 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00"}
		# The date is in a different format than the specified
		body9 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2023-11-05T08:15:30-05:00"}
		# The date is in a different format than the specified
		body10 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "November 5, 2023, 8:15:30 am"}
		# The data sent in cart_value is in an different format that the one expected.
		body11 = {"cart_value": "790", "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00"}
		# The data sent in delivery_distance is in an different format that the one expected.
		body12 = {"cart_value": 790, "delivery_distance": "2235", "number_of_items": 4, "time": "2024-01-15T13:00:00"}
		# The data sent in number_of_items is in an different format that the one expected.
		body13 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": "4", "time": "2024-01-15T13:00:00"}
		# The data sent in date is in an different format that the one expected.
		body14 = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": "4", "time": 172783674}
		listRequest = [body1, body2, body3, body4, body5, body6, body7, body8, body9, body10, body11, body12, body13, body14]
		for body in listRequest:
			response = self.client.post('/api/endpoint', json.dumps(body), content_type='application/json')
			self.assertEqual(response.status_code, 400)

	# This private method let us send different POST requests with different content of the body.
	# Also, it let us compare if the answers of every test matches with the answers sent by our endpoint.
	def	__testLoop(self, listRequest, answers):
		i = 0
		for body in listRequest:
			response = self.client.post('/api/endpoint', json.dumps(body), content_type='application/json')
			self.assertJSONEqual(str(response.content, encoding='utf8'), {"delivery_fee": answers[i]})
			i += 1
