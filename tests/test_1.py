import requests
import unittest
import random
import json
from config import ROOT_URL



symbols = "asdfghjklqwertyuiozxcvbnm1234567890"


class TestCreateUserCreatePublication(unittest.TestCase):
    def test_create_user(self):
        email = "".join(random.choices(symbols, k=random.randint(5,15)))
        password = "123456"
        name = "name"

        result = \
            requests.post(
                url=ROOT_URL+"create/user/",
                json={
                    'password': password,
                    'name': name,
                    'email': email
                },
                headers={
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                }
            )
        
        self.assertEqual(result.status_code, 200)
        self.user_data = json.loads(result.content.decode("utf-8"))
        result = \
            requests.post(
                url=ROOT_URL+"create/publication/",
                headers = {
                    'accept': 'application/json',
                    'user-id': str(self.user_data["id"]),
                    'user-token': self.user_data["token"],
                    'Content-Type': 'application/json',
                },

                json = {
                    'title': 'string',
                    'description': 'string',
                    'text': 'string',
                }
            )

        self.assertEqual(result.status_code, 200)
        self.data = result.content.decode("utf-8")
        print(self.data)
