from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .forms import Login_Form, Signup_Form, Deposit_Form, Withdraw_Form, Search_Form
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Custom_User
from portfolio.models import Portfolio, Holdings, Company
import requests
from .helpers import *

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)


@login_required(login_url="/login/")
def index(request):

    # request.user = Custom_User.objects.get(pk=request.user.pk)
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



# @login_required(login_url="/login/")

class Profile_view(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html',
            {
                'user': request.user,
                'deposit_form': Deposit_Form(),
                'withdraw_form': Withdraw_Form()
            }
        )

    def post(self, request, *args, **kwargs):
        # request.user = Custom_User.objects.get(pk=request.user.pk)
        deposit_form = Deposit_Form(request.POST)
        withdraw_form = Withdraw_Form(request.POST)

        # if request.method == "POST":

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

@login_required(login_url="/login/")
def add_to_following(request, company):

    # Do some logic:
    request.user.favorites += f',{company}'
    request.user.save()
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url="/login/")
def buy(request, company):
    data = fetchTicker(company)
    return render(request, 'buy.html', {'data': data})

@login_required(login_url="/login/")
def finish_buy(request, ticker):

    data = fetchTicker(ticker)
    P = Portfolio.objects.get(owner=request.user)
    C = Company.objects.filter(ticker_symbol=data['symbol'])
    H = P.Holdings.get(stock=C)

    if H:
        H.count += 1
        H.save()
    else:
        H = Holdings.objects.create(stock=C, count=1)
        H.save()
        request.user.portfolio.stocks.add(H)
        request.user.portfolio.save()

    return HttpResponseRedirect(reverse('index'))


# def login(request):
#     # if not request.user.is_authenticated:
#     #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#     return render(request, 'basic_form.html', {'form': Login_Form})

def login_view(request):
    html = 'basic_form.html'
    if request.method == 'POST':
        form = Login_Form(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = Login_Form()

    return render(request, html, {'form': form})

# def signup(request):
#     return render(request, 'basic_form.html', {'form': Signup_Form})


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def signup(request):
    html = 'basic_form.html'

    if request.method == 'POST':
        form = Signup_Form(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = Custom_User.objects.create_user(
                email=data['email'],
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
            )
            Portfolio.objects.create(
                name='',
                owner=user
            )
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = Signup_Form()
    return render(request, html, {'form': form})
