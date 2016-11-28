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
	# Checks that first champion in the champion rotation is ahri
	def test_champion_rotation(self):
		dict = processor.champion_rotation()
		dict = dict.data
		self.assertTrue(b'103' in dict)
	#checks that the champion rotation does not have invalid champions
	def test_champion_rotation_not(self):
		dict = processor.champion_rotation()
		dict = dict.data
		self.assertFalse(b'10000' in dict)
	#checks that the valid api method checks for a correct response from api	
	def test_valid_api_response_false(self):
		testResponse = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/Merky12345?api_key=" + processor.apiKey
		testResponse = requests.get(testResponse)
		self.assertFalse(processor.valid_api_request(testResponse))
	#checks that the valid api method check for a error response from api		
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
	#Checks that profile works for a valid username from a valid region
	def test_profile(self):
		processor.profile("na","faker")
		self.assert_template_used('profile.html')
		self.assert_context("name", "faker")
	#Checks that profile works even if the username is not level 30 (.ie doesn't have ranked stats available)
	def test_profile_level(self):
		processor.profile("na","bleedmaroon")
		self.assert_template_used('profile.html')
		self.assert_context("name", "bleedmaroon")
	#Checks that profile works for different regions such as EUW
	def test_profile_region(self):
		processor.profile("euw","rekkles")
		self.assert_template_used('profile.html')
		self.assert_context("name", "rekkles")
	#Checks that profile works for a username that has no mastery information / lacks mastery information
	def test_profile_no_mastery(self):
		processor.profile("na","sadfdsaf")
		self.assert_template_used('profile.html')
		self.assert_context("name", "sadfdsaf")
	#Checks that invalid username leads to the error page
	def test_profile_invalid(self):
		processor.profile("na","irtiza")
		self.assert_template_used('invalid.html')
		self.assert_context("error", "Error 404: No summoner data found for the specified inputs. Please try a different summoner name or region.")
	#Checks that the route to ultimate bravery works
	def test_ultimate_bravery(self):
		processor.ultimate_bravery()
		self.assert_template_used('ultimate-bravery.html')
	#Checks that the route to the free champion rotation works
	def test_free_champion_rotation(self):
		processor.free_champion_rotation()
		self.assert_template_used('free-champion-rotation.html')
	#Checks that the route to the index works
	def test_index(self):
		processor.index()
		self.assert_template_used('index.html')
	#Checks that the most recent game outputs an array of length 7.
	def test_recent_game(self):
		recent = processor.recent_game("na", "23629510")
		self.assertEqual(len(recent), 7)
		
if __name__ == '__main__':
	unittest.main()