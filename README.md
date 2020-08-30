# IG Markets Client
IG Markets API REST and Streaming Clients. The rest client only implements methods to retrieve price data only. 

LIVE account only.

To use the streaming client:

    session = IG_streaming_session(api_key='..', ulogin_details={'username':'..','password':'..'})
    px_subscription = Subscription('MERGE', ['MARKET:CS.D.BITCOIN.CFD.IP', 'MARKET:CS.D.ETHUSD.CFD.IP'],
                                   ['UPDATE_TIME', 'BID', 'OFFER'])
    px_subscription.addlistener(lambda item: print(item))
    session.subscribe(px_subscription)

    time.sleep(60)
    session.disconnect_session()

 
 
 
