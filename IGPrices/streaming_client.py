import logging
import traceback
import sys

from IGPrices.lighstreamer import LSClient
from IGPrices.rest_client import IGSession

logger = logging.getLogger(__name__)


class IG_streaming_session(IGSession, LSClient):
    def __init__(self, api_key: str, ulogin_details: dict):
        IGSession.__init__(self, api_key, ulogin_details)
        if self.login():
            self.connect_LSClient()

    def connect_LSClient(self):
        LSusername = self.login_details['username']
        LSpassword = f"CST-{self.authorisation_headers['CST']}|XST-{self.authorisation_headers['X-SECURITY-TOKEN']}"
        LSendpoint = self.lightstreamerEndpoint
        logger.info("Starting connection with %s" % LSendpoint)
        LSClient.__init__(self, LSendpoint, user=LSusername, password=LSpassword)
        try:
            self.connect()
        except Exception:
            logger.error("Unable to connect to Lightstreamer Server")
            logger.error(traceback.format_exc())
            sys.exit(1)
