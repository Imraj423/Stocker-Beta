from django.test import TestCase
from .helpers import *

class HelperTestCase(TestCase):

    def testFetchTicker(self):
        """ Test the ticker """
        aapl = fetchTicker('AAPL')
        amzn = fetchTicker('AMZN')
        msft = fetchTicker('MSFT')
        tsla = fetchTicker('TSLA')

        print(aapl)

    def testFetchCompany(self):
        """ Test the ticker """

    def testMultiFetcher(self):
        """ Test the ticker """