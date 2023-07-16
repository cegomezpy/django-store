from django.test import Client
from django.test import TestCase

class AuthTestCase(TestCase):
    def set_up(self):
        self.client = Client()
        self.login = self.client.login(name="U", password='12345678')
    
    def test_get_register_view(self):
        response = self.client.get('/Auth/')
        self.assertEquals(response.status_code, 200)

    def test_fail_login(self):
        pass