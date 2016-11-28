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
		
	def test_champion_rotation_not(self):
		dict = processor.champion_rotation()
		dict = dict.data
		self.assertFalse(b'10000' in dict)
		
	def test_valid_api_response_false(self):
		testResponse = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/Merky12345?api_key=" + processor.apiKey
		testResponse = requests.get(testResponse)
		self.assertFalse(processor.valid_api_request(testResponse))
			
	def test_valid_api_response_true(self):
		testResponse = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/Merky?api_key=" + processor.apiKey
		testResponse = requests.get(testResponse)
		self.assertTrue(processor.valid_api_request(testResponse))

	def test_valid_mastery_false(self):
		testMasteryInfo = []
		testMasteryInfo.append("0") #No Mastery so the score is 0
		self.assertEqual(len(testMasteryInfo), 1) #User has no mastery, so they have no entries
		testMasteryInfo = processor.valid_mastery(testMasteryInfo) #Check if valid amount of entries
		self.assertEqual(len(testMasteryInfo), 6)  #There isn't valid amount of entries, so it fills "0" entries

	def test_valid_mastery_true(self):
		testMasteryInfo = []
		subInfo = []
		testMasteryInfo.append("237")   #Add Total Mastery score
		testMasteryInfo.append(subInfo) #Add #1 Champion based on mastery
		testMasteryInfo.append(subInfo) #Add #2 Champion based on mastery
		testMasteryInfo.append(subInfo) #Add #3 Champion based on mastery
		testMasteryInfo.append(subInfo) #Add #4 Champion based on mastery
		testMasteryInfo.append(subInfo) #Add #5 Champion based on mastery
		self.assertEqual(len(testMasteryInfo), 6) #Size should be for
		testMasteryInfo = processor.valid_mastery(testMasteryInfo) #Mastery has valid amount of information
		self.assertEqual(len(testMasteryInfo), 6)                  #So it should remained unchanged.

	def test_profile(self):
		response = processor.profile("na", "blitzkriegzz")
		print(response)

	def test_champion_info(self):
		app = self.create_app()
		tester = app.test_client()
		response = tester.get('/champion_info', headers=[('X-Requested-With'), ('XMLHttpRequest')])
		response = response.data
		print('response')

	def test_recent_game(self):
		recent = processor.recent_game("na", "23629510")
		#print(recent)
		self.assertEqual(len(recent), 7)
		
if __name__ == '__main__':
	unittest.main()