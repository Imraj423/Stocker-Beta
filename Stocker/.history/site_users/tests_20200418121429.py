from django.test import TestCase
from .helpers import *

class HelperTestCase(TestCase):

    def testFetchTicker(self):
        """ Test the ticker """
        aapl = fetchTicker('AAPL')
        amzn = fetchTicker('AMZN')
        msft = fetchTicker('MSFT')
        tsla = fetchTicker('TSLA')


        self.assertEqual(aapl['symbol'], 'AAPL')
        self.assertEqual(amzn['symbol'], 'AMZN')
        self.assertEqual(msft['symbol'], 'MSFT')
        self.assertEqual(tsla['symbol'], 'TSLA')

    def testFetchCompany(self):
        """ Test the ticker """

    def testMultiFetcher(self):
        """ Test the ticker """