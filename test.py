import unittest
import datetime
from pandas.tseries.offsets import BDay

from IGPrices.rest_client import IGSession
from IGPrices.utilities import conv_datetime
import secrets
from IGPrices.config import IG_BASE_URL


def get_session():
    login_details = {'username': secrets.username, 'password': secrets.password}
    return IGSession(IG_BASE_URL, secrets.API_key, login_details)


class MyTestCase(unittest.TestCase):
    def test_login(self):
        session = get_session()
        session.login()
        self.assertIsNotNone(session.authorization_headers)

    def test_search_markets(self):
        session = get_session()
        data = session.search_markets("ASX")
        self.assertEqual(data.shape[0], 46)

    def test_epic_price(self):
        numpoints = 5
        session = get_session()
        data = session.get_historical_prices(epic_id="CS.D.AUDUSD.CFD.IP", numpoints=numpoints)
        self.assertEqual(data.shape[0], numpoints)

    def test_fixed_price(self):
        numpoints = 5
        session = get_session()
        data = session.get_historical_prices(method="FIXED", epic_id="CS.D.AUDUSD.CFD.IP", numpoints=numpoints)
        self.assertEqual(data.shape[0], numpoints)

    def test_date_price(self):
        start_date = datetime.datetime.today()-BDay(1)
        start_date_rounded = start_date - datetime.timedelta(minutes=start_date.minute % 1,
                                     seconds=start_date.second,
                                     microseconds=start_date.microsecond)
        end_date = datetime.datetime.today()
        end_date_rounded = end_date - datetime.timedelta(minutes=end_date.minute % 1,
                                     seconds=end_date.second,
                                     microseconds=end_date.microsecond)
        session = get_session()
        data = session.get_historical_prices(method="DATE", epic_id="CS.D.AUDUSD.CFD.IP", start_date=start_date_rounded, end_date=end_date_rounded)
        self.assertEqual(conv_datetime(data['snapshotTime'].iloc[0], 1), conv_datetime(start_date_rounded, 1))
        self.assertEqual(conv_datetime(data['snapshotTime'].iloc[-1], 1), conv_datetime(end_date_rounded, 1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
