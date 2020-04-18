from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import Login_Form, Signup_Form, Deposit_Form, Withdraw_Form, Search_Form
from .models import Custom_User
import requests
from .helpers import *


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
                amount = do_form_stuff(deposit_form)['deposit']
                current_usr.deposits += amount
                current_usr.save()

            elif withdraw_form.is_valid():
                amount = do_form_stuff(withdraw_form)['withdraw']
                current_usr.withdraws -= amount
                current_usr.save()

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


def finish_buy(request, ticker):
    return HttpResponseRedirect(reverse('index'))


def analysis(request, company):
    # Dead ass last, this may not happen at all
    # return render(request, 'analysis.html')
    pass


def login(request):
    return render(request, 'basic_form.html', {'form': Login_Form})


def signup(request):
    return render(request, 'basic_form.html', {'form': Signup_Form})