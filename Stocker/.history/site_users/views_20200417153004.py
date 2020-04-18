from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import Login_Form, Signup_Form, Deposit_Form, Withdraw_Form, Search_Form
from .models import Custom_User
from portfolio.models import Company
import requests


# Get me out of views
def fetchCompanyData(ticker):
    r = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker}/company?token=pk_8b849948242d4bb38c80005cdf53f2a6')
    return r.json()


# Get me out of views
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


# Get me out of views
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


# class
def index(request):

    current_usr = Custom_User.objects.get(pk=request.user.pk)
    follow_list = current_usr.favorites.split(',')[1:]
    follow_data = multiFetcher(follow_list)
    company_data = [fetchCompanyData(tkr) for tkr in follow_list]
    search_form = Search_Form(request.POST)

    #refactor {following, and company}

    if request.method == "POST":
        if search_form.is_valid():
            data = search_form.cleaned_data
            ticker = data['ticker']
            stock_data = fetchTicker(ticker)
            return render(request, 'index.html', 
                        {
                            'form': search_form,
                            'data': stock_data,
                            'following': follow_data,
                            'company': company_data
                        })

    return render(request, 'index.html', 
                    {
                        'form': search_form,
                        'following': follow_data,
                        'company': company_data
                    })

# class
# when we need differend HTTP VERBS
def profile(request):

    current_usr = Custom_User.objects.get(pk=request.user.pk)
    deposit_form = Deposit_Form(request.POST)
    withdraw_form = Withdraw_Form(request.POST)

    if request.method == "POST":

        def do_form_stuff(f):
            form = f
            return form.cleaned_data

        if deposit_form.is_valid() or withdraw_form.is_valid():
            
            if deposit_form.is_valid():
                amount = int(do_form_stuff(deposit_form)['dep_amount'])
                current_usr.deposits += amount
            
            elif withdraw_form.is_valid():
                amount = int(do_form_stuff(withdraw_form)['wtd_amount'])
                current_usr.withdraws -= amount
            else:
                return 'Should not be able to get here'

    return render(request, 'profile.html', 
                    {
                        'user': current_usr, 
                        'deposit_form': deposit_form,
                        'withdraw_form': withdraw_form
                    })


def add_to_following(request, company):

    # Do some logic:
    request.user.favorites += f',{company}'
    request.user.save()
    return HttpResponseRedirect(reverse('index'))


def buy(request, company):
    data = fetchTicker(company)
    return render(request, 'buy.html', {'data': data})


def finishBuy(request, ticker):
    amount = '??'
    price = request.user.portfolio.stocks.filter('???')
    total = amount * price

    return HttpResponseRedirect(reverse('index'))


def analysis(request, company):
    # Dead ass last, this may not happen at all
    # return render(request, 'analysis.html')
    pass


def login(request):
    return render(request, 'basic_form.html', {'form': Login_Form})


def signup(request):
    return render(request, 'basic_form.html', {'form': Signup_Form})