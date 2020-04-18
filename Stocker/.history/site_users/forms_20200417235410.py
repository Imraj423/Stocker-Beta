from django import forms


class Login_Form(forms.Form):
    display_name = forms.CharField(max_length=42)
    password = forms.CharField(max_length=42)


# model form
class Signup_Form(forms.Form):
    email = forms.EmailField()
    display_name = forms.CharField(max_length=42)
    first_name = forms.CharField(max_length=42)
    last_name = forms.CharField(max_length=42)
    password = forms.CharField(max_length=42)


class Deposit_Form(forms.Form):
    dep_amount = forms.IntegerField()


class Withdraw_Form(forms.Form):
    wtd_amount = forms.IntegerField()


class Search_Form(forms.Form):
    ticker = forms.CharField(max_length=5)

