from django.test import TestCase
from .helpers import *

class HelperTestCase(TestCase):
    def testFetchTicker(self):
        """
        Test that the data returned is a dict
        and that the correct ticker is returned
        from the network request.
        """
        aapl = fetchTicker('AAPL')
        amzn = fetchTicker('AMZN')
        msft = fetchTicker('MSFT')
        tsla = fetchTicker('TSLA')

        self.assertTrue(isinstance(aapl, dict))
        self.assertTrue(isinstance(amzn, dict))
        self.assertTrue(isinstance(msft, dict))
        self.assertTrue(isinstance(tsla, dict))

        self.assertEqual(aapl['symbol'], 'AAPL')
        self.assertEqual(amzn['symbol'], 'AMZN')
        self.assertEqual(msft['symbol'], 'MSFT')
        self.assertEqual(tsla['symbol'], 'TSLA')

    def testFetchCompany(self):
        """
        Test the ticker
        """
        aapl = fetchCompanyData('AAPL')
        amzn = fetchCompanyData('AMZN')
        msft = fetchCompanyData('MSFT')
        tsla = fetchCompanyData('TSLA')

        self.assertTrue(isinstance(aapl, dict))
        self.assertTrue(isinstance(amzn, dict))
        self.assertTrue(isinstance(msft, dict))
        self.assertTrue(isinstance(tsla, dict))

        self.assertEqual(aapl['symbol'], 'AAPL')
        self.assertEqual(amzn['symbol'], 'AMZN')
        self.assertEqual(msft['symbol'], 'MSFT')
        self.assertEqual(tsla['symbol'], 'TSLA')

        self.assertNotEqual(aapl['companyName'], '')
        self.assertNotEqual(aapl['industry'], '' )
        self.assertNotEqual(aapl['website'], '') 
        self.assertNotEqual(aapl['description'], '')

    def testMultiFetcher(self):
        """ Test the Multifetcher """
        stock_list = multiFetcher(['amzn', 'aapl', 'tsla', 'msft'])

