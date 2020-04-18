from django.db import models
from django.apps import apps
from django.contrib.auth.models import AbstractUser
from portfolio.models import Portfolio

class Custom_User(AbstractUser):
    email = models.EmailField()
    display_name = models.CharField(max_length=42)
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    
    # in pennies, not dollars
    deposits = models.DecimalField(decimal_places=2, max_digits=8, null=True , default=Decimal('0.00'))
    withdraws = models.DecimalField(decimal_places=2, max_digits=8, null=True, default=Decimal('0.00'))

    favorites = models.CharField(max_length=599)
