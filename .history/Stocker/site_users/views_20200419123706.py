from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import Login_Form, Signup_Form, Deposit_Form, Withdraw_Form, Search_Form
from .models import Custom_User
from portfolio.models import Portfolio, Holdings, Company
import requests
from django.contrib.auth.decorators import login_required
from .helpers import *


# class
@login_required(login_url='/login/')
def index(request):

    # current_usr = Custom_User.objects.get(pk=request.user.pk)
    follow_list = request.user.favorites.split(',')[1:]
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
                        'company': company_data,
                        'portfolio': request.user.portfolio.stocks.all() 
                    })

# class
# when we need differend HTTP VERBS
@login_required(login_url='/login/')
def profile(request):

    # current_usr = Custom_User.objects.get(pk=request.user.pk)
    deposit_form = Deposit_Form(request.POST)
    withdraw_form = Withdraw_Form(request.POST)

    if request.method == "POST":

        def do_form_stuff(f):
            form = f
            return form.cleaned_data

        if deposit_form.is_valid() or withdraw_form.is_valid():
            
            if deposit_form.is_valid():
                amount = do_form_stuff(deposit_form)['deposit']
                request.user.deposits += amount
                request.user.save()

            elif withdraw_form.is_valid():
                amount = do_form_stuff(withdraw_form)['withdraw']
                request.user.withdraws -= amount
                request.user.save()

            else:
                return 'Should not be able to get here'

    return render(request, 'profile.html', 
                    {
                        'user': request.user, 
                        'deposit_form': deposit_form,
                        'withdraw_form': withdraw_form
                    })


@login_required(login_url='login/')
def add_to_following(request, company):

    # Do some logic:
    request.user.favorites += f',{company}'
    request.user.save()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login/')
def buy(request, company):
    data = fetchTicker(company)
    return render(request, 'buy.html', {'data': data})


@login_required(login_url='login/')
def finish_buy(request, ticker):

    data = fetchTicker(ticker)
    P = Portfolio.objects.filter(owner=request.user)
    if len(P) <= 0:
        P = Portfolio.objects.create(owner=request.user)   
    C = Company.objects.get(ticker_symbol=data['symbol'])
    H = Holdings.objects.create(stock=C, count=5)

    request.user.portfolio.stocks.add(H)
    request.user.portfolio.save()

    return HttpResponseRedirect(reverse('index'))


def analysis(request, company):
    # Dead ass last, this may not happen at all
    # return render(request, 'analysis.html')
    pass


def login(request):
    return render(request, 'basic_form.html', {'form': Login_Form})


def signup(request):
    return render(request, 'basic_form.html', {'form': Signup_Form})