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
    deposit = models.DecimalField(decimal_places=2, max_digits=8, null=True)


class Withdraw_Form(forms.Form):
    withdraw = models.DecimalField(decimal_places=2, max_digits=8, null=True)


class Search_Form(forms.Form):
    ticker = forms.CharField(max_length=5)
