from datetime import datetime
from pandas.tseries.offsets import BDay

if __name__ == '__main__':
    from IGPrices.rest_client import IGSession
    import secrets
    from IGPrices import config

    login_details = {'username': secrets.login_details['username'], 'password': secrets.login_details['password']}
    session = IGSession(secrets.API_key, login_details)

    start_date = datetime.today() - BDay(10)
    end_date = datetime.today() - BDay(4)

    # data = session.get_historical_prices(
    #                                     epic_id='CS.D.CFDGOLD.CFDGC.IP',
    #                                     # method='DATE',
    #                                     resolution='DAY',
    #                                     # start_date=start_date,
    #                                     end_date=end_date,
    #                                     numpoints=100,
    #                                     pagesize=100)
    data = session.search_markets('Gold')
    # data = session.get_market_details('CS.D.CFDGOLD.CFDGC.IP')
    # print(data['epic'])
    print(data.loc[1])
    # print(data['instrumentType'].unique())
    #start_date = datetime.today()-BDay(1)
    #end_date = datetime.today()
    #data = session.get_historical_prices(method="DATE", epic_id="CS.D.AUDUSD.CFD.IP", start_date=start_date, end_date=end_date)
