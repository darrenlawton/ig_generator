from IGPrices.lightstreamer import Subscription
from IGPrices.rest_client import IG_session
from IGPrices.streaming_client import IG_streaming_session
import secrets
import time


def get_session():
    login_details = {'username': secrets.login_details['username'], 'password': secrets.login_details['password']}
    session = IG_session(secrets.API_key, login_details)
    data = session.search_markets("Ether")
    print(data.loc[0])


if __name__ == '__main__':
    # get_session()
    session = IG_streaming_session(api_key=secrets.API_key, ulogin_details=secrets.login_details)

    px_subscription = Subscription('MERGE', ['MARKET:CS.D.BITCOIN.CFD.IP', 'MARKET:CS.D.ETHUSD.CFD.IP'],
                                   ['UPDATE_TIME', 'BID', 'OFFER'])
    px_subscription.addlistener(lambda item: print(item))
    session.subscribe(px_subscription)

    time.sleep(60)
    session.disconnect_session()