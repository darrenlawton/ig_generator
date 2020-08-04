if __name__ == '__main__':
    from src.rest_client import IGSession
    import secrets
    from src import config

    login_details = {'username': secrets.username, 'password': secrets.password}
    session = IGSession(config.IG_BASE_URL, secrets.API_key, login_details)
    # data = session.search_markets("AUDUSD")
    print(session.get_historical_prices(method="DATE", epic_id="CS.D.AUDUSD.CFD.IP"))