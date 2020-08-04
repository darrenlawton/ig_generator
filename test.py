import unittest
from src.rest_client import IGSession
import secrets
from src.config import IG_BASE_URL


class MyTestCase(unittest.TestCase):
    def test_login(self):
        login_details = {'username': secrets.username, 'password': secrets.password}
        session = IGSession(IG_BASE_URL, secrets.API_key, login_details)
        session.login()
        self.assertIsNotNone(session.authorization_headers)

    def test_search_markets(self):
        login_details = {'username': secrets.username, 'password': secrets.password}
        session = IGSession(IG_BASE_URL, secrets.API_key, login_details)
        data = session.search_markets("ASX")
        self.assertEqual(data.shape[0], 46)


if __name__ == '__main__':
    unittest.main(verbosity=2)
