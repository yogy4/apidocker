import os
import unittest
from flask import json
from base64 import b64encode
from app import backserv, db

class BajuApi(unittest.TestCase):
    email = 'em@test.co'
    password = 'passtest'
   
    def setUp(self):
        backserv.config.from_object(os.environ['TEST_SETTINGS'])
        self.backserv =  backserv.test_client()        
        self.assertEqual(backserv.debug, False)

    def tearDown(self):
        pass

    def authenticate_user(self, email, password):
        auth = 'Basic ' + b64encode((email + ':' + password).encode('utf-8')).decode('utf-8')
        headers = {}
        headers['Authorization'] = auth
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        return self.backserv.get('/get-auth-token', headers=headers)

    def get_headers_authenticated(self):
        headers = {}
        response = self.authenticate_user(self.email, self.password)
        json_data = json.loads(response.data.decode('utf-8'))
        auth = 'Basic ' + b64encode((json_data['token'] + ':' + 'unused').encode('utf-8')).decode('utf-8')
        headers['Authorization'] = auth
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        return headers

    def test_login_valid(self):
        response = self.authenticate_user(self.email, self.password)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'token', response.data)
        self.assertIn('private', response.headers['Cache-Control'])
        self.assertIn('no-cache', response.headers['Cache-Control'])
        self.assertIn('no-store', response.headers['Cache-Control'])
        self.assertIn('max-age=0', response.headers['Cache-Control'])

    def test_login_invalid(self):
        response = self.authenticate_user(self.email, self.password)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertIn('unauthorized', json_data['error'])
        self.assertIn('please authenticate', json_data['message'])

    def test_invalid_authentication_user(self):
        response = self.authenticate_user(self.email, 'anoemail')
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertIn('Unauthorized', json_data['error'])
        self.assertIn('Please authenticate', json_data['message'])

    def test_invalid_token(self):
        headers = {}
        response = self.authenticate_user(self.password, 'anopass')
        json_data = json.loads(response.data.decode('utf-8'))
        token = 'InvalidTokenInvalidToken'
        auth = 'Basic ' + b64encode((token + ':' + 'unused').encode('utf-8')).decode('utf-8')
        headers['Authorization'] = auth
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        response = self.backserv.get('/api/baju', headers=headers)

        self.assertEqual(response.status_code, 401)

    def test_baju_get_all(self):
        headers = self.get_headers_authenticated()
        response = self.backserv.get('/api/baju', headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_baju_create(self):
        headers = self.get_headers_authenticated()
        json_data = {'name': 'bj22', 'size': 'M', 'price': 50000, 'quantity': 4}
        response = self.backserv.post('/api/baju', data=json.dumps(json_data), headers=headers, follow_redirects=True)

        self.assertEqual(response.status_code, 201)
        self.assertIn('/api/baju/2', response.headers['Location'])

    def test_baju_get_by_id_valid(self):
        headers = self.get_headers_authenticated()
        response = self.backserv.get('/api/baju/1', headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Ripc', json_data['name'])
        self.assertIn('M', json_data['size'])
        self.assertIn(30000, json_data['price'])
        self.assertIn(4, json_data['quantity'])
        self.assertIn('api/baju/1', json_data['self_url'])

    def test_baju_get_by_id_invalid(self):
        headers = self.get_headers_authenticated()
        response = self.backserv.get('/api/baju/5', headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('invalid ', json_data['message'])
        self.assertIn('not found', json_data['error'])  

    def test_baju_update_valid(self):
        headers = self.get_headers_authenticated()
        json_data = {'name': 'Clothes change', 'size': 'L'}
        response = self.backserv.put('/api/baju/4', data=json.dumps(json_data), headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('success', json_data['result'])

    def test_baju_update_invalid(self):
        headers = self.get_headers_authenticated()
        json_data_input = {'name': 'Clothes change', 'size': 'LL'}
        response = self.backserv.put('/api/baju/8', data=json.dumps(json_data_input), headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('invalid resource', json_data['message'])
        self.assertIn('not found', json_data['error'])

    def test_baju_delete_valid(self):
        headers = self.get_headers_authenticated()
        response = self.backserv.delete('/api/baju/2', headers=headers)

        self.assertEqual(response.status_code, 200)

    def test_baju_delete_invalid(self):
        headers = self.get_headers_authenticated()
        response = self.backserv.delete('/api/baju/6', headers=headers)
        json_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn('invalid', json_data['message'])
        self.assertIn('not found', json_data['error'])

    
# if __name__ == "__main__":
#     unittest.main()
