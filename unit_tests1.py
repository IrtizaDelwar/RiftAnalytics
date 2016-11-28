import requests
from flask import Flask
import processor
import unittest
import json

# To test please run "python unit_tests1.py -v" in your command prompt.
# Also ensure that you have requests, blinker, and flask-testing installed. (ie. pip install requests)
# Testing with LiveServer
class MyTest(unittest.TestCase):
  # if the create_app is not implemented NotImplementedError will be raised
    def setUp(self):
        # Create Flask test client
        processor.app.config['TESTING'] = True
        self.app = processor.app.test_client()
    #Testing if the champion_Info() method works. This method takes in a champion id and returns a name, description, and image.
    #The champion IDs are chosen from random from an array of hardcoded ids. So it is not possible to get an invalid id.
    def test_champion_info(self):
        response = self.app.post('/champion_info', data=dict(id = '266'))
        response = response.data
        self.assertIn(b'Aatrox', response)
        self.assertIn(b'the Darkin Blade', response)
        self.assertIn(b'Aatrox.png', response)
    #Tests a second ID to make sure. This champion has a space in it's name to make sure there is no problem.
    def test_champion_info2(self):
        response = self.app.post('/champion_info', data=dict(id = '223'))
        response = response.data
        self.assertIn(b'Tahm Kench', response)
        self.assertIn(b'the River King', response)
        self.assertIn(b'TahmKench.png', response)
    #Testing if the item_info() method works. This method takes in a item id and return it's name, and image.
    #The item IDs are chosen from random from an array of hardcoded Ids. So it is not possible to get an invalid id.
    def test_item_info(self):
        response = self.app.post('/item_info', data=dict(id = '3001'))
        response = response.data
        self.assertIn(b'Abyssal Scepter', response)
        self.assertIn(b'3001.png', response)
    #Making sure than an ID from the boot array also works for this method. This id has a ' character in it.
    def test_item_info2(self):
        response = self.app.post('/item_info', data=dict(id = '3006'))
        response = response.data
        self.assertIn(b'Berserker\'s Greaves', response)
        self.assertIn(b'3006.png', response)
    #Testing if the spell_info() method works. This method takens in 2 spell id's and returns their name and image.
    #The spell IDs are chosen from random from an array of hardcoded Ids. So it is not possible to get an invalid id.
    def test_sspell_info(self):
        response = self.app.post('/sspell_info', data=dict(id = '21', id2 = '1'))
        response = response.data
        self.assertIn(b'Barrier', response)
        self.assertIn(b'SummonerBarrier.png', response)
        self.assertIn(b'Cleanse', response)
        self.assertIn(b'SummonerBoost.png', response)
    #Tests other spells to make sure they work.
    def test_sspell_info2(self):
        response = self.app.post('/sspell_info', data=dict(id = '13', id2 = '14'))
        response = response.data
        self.assertIn(b'Clarity', response)
        self.assertIn(b'SummonerMana.png', response)
        self.assertIn(b'Ignite', response)
        self.assertIn(b'SummonerDot.png', response)
     #The following 3 tests is for get_error. If an error occured then the response would be an html. If no error, then response would be json type
    def test_champion_info_not(self):
        response = self.app.post('/champion_info', data=dict(id = '10000'))
        self.assertEqual(response.mimetype, 'text/html')
    
    def test_item_info_not(self):
        response = self.app.post('/item_info', data=dict(id = '10000'))
        self.assertEqual(response.mimetype, 'text/html')
    
    def test_sspell_info_not(self):
        response = self.app.post('/sspell_info', data=dict(id = '10000', id2 = '10000'))
        self.assertEqual(response.mimetype, 'text/html')
		
if __name__ == '__main__':
    unittest.main()