def fetchCompanyData(ticker):
    r = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker}/company?token=pk_8b849948242d4bb38c80005cdf53f2a6')
    return r.json()


def fetchTicker(ticker):
    r = requests.get(f'https://sandbox.iexapis.com/stable/stock/{ticker}/quote?token=Tpk_40ebc98b6181404fac1a900fa92b4690')

    co = Company.objects.filter(ticker_symbol=ticker).first()
    if co:
        co.price = r.json()['latestPrice']
        co.save()
    else:
        Company.objects.create(name=r.json()['companyName'], 
                               ticker_symbol=r.json()['symbol'], 
                               price=r.json()['latestPrice'])

    return r.json()

def multiFetcher(follow_list):
    stock_tickers = []
    for tkr in follow_list:        
        data = fetchTicker(tkr)
        stock_tickers.append({
            'symbol': tkr,
            'company': data['companyName'],
            'price': data['latestPrice'],
            'change': data['change']
        })
    return stock_tickers