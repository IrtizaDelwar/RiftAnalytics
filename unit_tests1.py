import requests
from flask import Flask
import processor
import unittest
import json

# Testing with LiveServer
class MyTest(unittest.TestCase):
  # if the create_app is not implemented NotImplementedError will be raised
    def setUp(self):
        # Create Flask test client
        processor.app.config['TESTING'] = True
        self.app = processor.app.test_client()

    def test_champion_info(self):
        response = self.app.post('/champion_info', data=dict(id = '266'))
        response = response.data
        self.assertIn(b'Aatrox', response)
        self.assertIn(b'the Darkin Blade', response)
        self.assertIn(b'Aatrox.png', response)
    
    def test_item_info(self):
        response = self.app.post('/item_info', data=dict(id = '3001'))
        response = response.data
        self.assertIn(b'Abyssal Scepter', response)
        self.assertIn(b'3001.png', response)
    
    def test_sspell_info(self):
        response = self.app.post('/sspell_info', data=dict(id = '21', id2 = '1'))
        response = response.data
        self.assertIn(b'Barrier', response)
        self.assertIn(b'SummonerBarrier.png', response)
        self.assertIn(b'Cleanse', response)
        self.assertIn(b'SummonerBoost.png', response)
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