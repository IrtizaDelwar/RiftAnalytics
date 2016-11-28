import requests
from flask import Flask
from flask_testing import TestCase 
import processor
import unittest
import json

# Testing with LiveServer
class MyTest(TestCase):
  # if the create_app is not implemented NotImplementedError will be raised
	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		return app 
			
	def test_champion_rotation(self):
		dict = processor.champion_rotation()
		dict = dict.data
		#print(dict)
		self.assertTrue(b'103' in dict)
		
	def test_valid_api_response_false(self):
		testResponse = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/Merky12345?api_key=" + processor.apiKey
		testResponse = requests.get(testResponse)
		self.assertFalse(processor.valid_api_request(testResponse))
			
	def test_valid_api_response_true(self):
		testResponse = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/Merky?api_key=" + processor.apiKey
		testResponse = requests.get(testResponse)
		self.assertTrue(processor.valid_api_request(testResponse))
		
if __name__ == '__main__':
	unittest.main()