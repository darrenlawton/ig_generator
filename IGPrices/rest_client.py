import json
import logging
import traceback
from abc import abstractmethod, ABC
from urllib.parse import urljoin
from requests import request
import pandas as pd
import datetime
from pandas.tseries.offsets import BDay

import IGPrices.config as config
from IGPrices.utilities import update_headers, encrypt_password, conv_datetime

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=config.LOGGING_LEVEL)


class BaseClient(ABC):
    def get(self, endpoint: str, **kwargs) -> dict:
        return self.ig_request('GET', endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> dict:
        return self.ig_request('POST', endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> dict:
        return self.ig_request('PUT', endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> dict:
        return self.ig_request('DELETE', endpoint, **kwargs)

    @abstractmethod
    def ig_request(self, method: str, endpoint: str, params: dict = None, data: dict = None,
                   headers: dict = None) -> dict: pass


class IGSession(BaseClient):
    def __init__(self, api_key: str, ulogin_details: dict):
        self.base_url = 'https://api.ig.com/gateway/deal/'
        self.api_key = api_key
        self.login_details = ulogin_details

        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json; charset=UTF-8',
                        'X-IG-API-KEY': self.api_key}
        self.authorisation_headers = {'CST': None,
                                      'X-SECURITY-TOKEN': None}
        self.lightstreamerEndpoint = None

    def login(self) -> bool:
        key, timestamp = self.get_encryption_key(self.login_details['username'])
        epassword, encryption = encrypt_password(self.login_details['password'], key, timestamp)

        try:
            response = request('POST', urljoin(self.base_url, 'session'),
                               data=json.dumps(
                                   {'encryptedPassword': encryption, 'identifier': self.login_details['username'],
                                    'password': epassword}),
                               headers={**self.headers, 'Version': '2'}, timeout=config.API_TIMEOUT)
            if response.status_code == 200:
                self.authorisation_headers = update_headers(self.authorisation_headers, response.headers)
                self.lightstreamerEndpoint = response['lightstreamerEndpoint']
                return True
            else:
                logging.error("Login Error: {0} {1}".format(response.status_code, response.text))
        except Exception as e:
            logging.error(traceback.format_exc())
            raise e
        return False

    def logout(self) -> None:
        self.delete('session', headers={})

    def get_encryption_key(self, identifier):
        try:
            response = request('GET', urljoin(self.base_url, config.IG_ENCRYPT_ENDPOINT),
                               headers={**self.headers}, timeout=config.API_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                return data["encryptionKey"], data["timeStamp"]
            else:
                logging.error("Encryption key error: {0} {1}".format(response.status_code, response.text))
        except Exception as e:
            logging.error(traceback.format_exc())
            raise e

        return None, None

    def ig_request(self, method: str, endpoint: str, params: dict = None, data: dict = None,
                   headers: dict = None) -> dict:
        if None in list(self.authorisation_headers.values()):
            self.login()

        ig_headers = {**self.headers, **self.authorisation_headers}
        if headers is not None:
            ig_headers.update(headers)

        if data is not None:
            data = json.dumps(data)

        try:
            response = request(method, urljoin(self.base_url, endpoint), params=params,
                               data=data, headers=ig_headers, timeout=config.API_TIMEOUT)
            if response.status_code == 200:
                self.authorisation_headers = update_headers(self.authorisation_headers, response.headers)
                if response.content:
                    return response.json()
                else:
                    return {}
            else:
                logging.error("IG request error: {0} {1}".format(response.status_code, response.text))
        except Exception as e:
            logging.error(traceback.format_exc())
            raise e

    def search_markets(self, search_term) -> pd.DataFrame:
        endpoint = "markets"
        params = {"searchTerm": search_term}
        data = self.get(endpoint=endpoint, params=params)
        if data is not None:
            return pd.DataFrame(data["markets"])
        else:
            None

    def get_market_details(self, epic_id) -> dict():
        endpoint = urljoin("markets/", epic_id)
        data = self.get(endpoint=endpoint)
        if data is not None:
            return data
        else:
            None

    def history_by_epic(self, epic_id, resolution, start_date, end_date, numpoints, pagesize,
                        pagenumber) -> pd.DataFrame:
        # https://labs.ig.com/rest-trading-api-reference/service-detail?id=521
        endpoint = urljoin("prices/", epic_id)
        params = {'version': "3"}
        if resolution: params['resolution'] = resolution
        if start_date: params['from'] = conv_datetime(start_date, 3)
        if end_date: params['to'] = conv_datetime(end_date, 3)
        if numpoints: params['max'] = numpoints
        if pagesize: params["pageSize"] = pagesize
        if pagenumber: params["pageNumber"] = pagenumber

        data = self.get(endpoint=endpoint, params=params)
        if data is not None:
            return pd.DataFrame(data["prices"])
        else:
            None

    def history_by_fixed(self, epic_id, resolution, start_date, end_date, numpoints, pagesize,
                         pagenumber) -> pd.DataFrame:
        # https://labs.ig.com/rest-trading-api-reference/service-detail?id=552
        if resolution is None: resolution = "MINUTE"
        if numpoints is None: numpoints = 10
        endpoint = "prices/" + epic_id + "/" + resolution + "/" + str(numpoints)
        params = {'version': "1"}

        data = self.get(endpoint=endpoint, params=params)
        if data is not None:
            return pd.DataFrame(data["prices"])
        else:
            None

    def history_by_date(self, epic_id, resolution, start_date, end_date, numpoints, pagesize,
                        pagenumber) -> pd.DataFrame:
        # https://labs.ig.com/rest-trading-api-reference/service-detail?id=538
        if start_date is None: start_date = datetime.datetime.today() - BDay(1)
        if end_date is None: end_date = datetime.datetime.today()
        if resolution is None: resolution = "MINUTE"

        endpoint = "prices/" + epic_id + "/" + resolution
        params = {'version': "1",
                  "startdate": conv_datetime(start_date, 1),
                  "enddate": conv_datetime(end_date, 1)}

        data = self.get(endpoint=endpoint, params=params)
        if data is not None:
            return pd.DataFrame(data["prices"])
        else:
            None

    def get_historical_prices(self, epic_id, method='EPIC', resolution=None,
                              start_date=None, end_date=None, numpoints=None,
                              pagesize=0, pagenumber=None) -> pd.DataFrame:
        method_history = config.PRICE_HISTORY
        if method not in method_history.keys():
            logging.warning("Method not recognised - select EPIC, FIXED or DATE.")
            return None

        switcher = {
            'EPIC': self.history_by_epic,
            'FIXED': self.history_by_fixed,
            'DATE': self.history_by_date
        }

        func = switcher.get(method)
        return func(epic_id, resolution, start_date, end_date, numpoints, pagesize, pagenumber)
