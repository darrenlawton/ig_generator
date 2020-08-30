import logging
import traceback
import sys

from IGPrices.lightstreamer import LSClient
from IGPrices.rest_client import IG_session

logger = logging.getLogger(__name__)


class IG_streaming_session(IG_session, LSClient):
    def __init__(self, api_key: str, ulogin_details: dict):
        IG_session.__init__(self, api_key, ulogin_details)
        if self.login():
            self.connect_lsclient()

    def connect_lsclient(self):
        ls_username = self.login_details['username']
        ls_password = f"CST-{self.authorisation_headers['CST']}|XST-{self.authorisation_headers['X-SECURITY-TOKEN']}"
        ls_endpoint = self.lightstreamerEndpoint
        logger.info("Starting connection with %s" % ls_endpoint)
        LSClient.__init__(self, ls_endpoint, user=ls_username, password=ls_password)
        try:
            self.connect()
        except Exception as e:
            logger.error("Unable to connect to Lightstreamer Server")
            logger.error(traceback.format_exc())
            raise e

    def disconnect_session(self):
        # disconnect from LS server
        self.disconnect()
        # log out of IG session
        self.logout()