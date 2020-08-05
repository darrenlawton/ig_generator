from datetime import datetime
from pandas.tseries.offsets import BDay

if __name__ == '__main__':
    from IGPrices.rest_client import IGSession
    import secrets
    from IGPrices import config

    login_details = {'username': secrets.username, 'password': secrets.password}
    session = IGSession(config.IG_BASE_URL, secrets.API_key, login_details)
    start_date = datetime.today()-BDay(1)
    end_date = datetime.today()
    data = session.get_historical_prices(method="DATE", epic_id="CS.D.AUDUSD.CFD.IP", start_date=start_date, end_date=end_date)
