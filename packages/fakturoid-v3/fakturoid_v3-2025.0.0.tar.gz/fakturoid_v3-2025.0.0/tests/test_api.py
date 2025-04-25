from __future__ import absolute_import

import unittest
from datetime import date
from unittest.mock import patch

from fakturoid import Fakturoid

from tests.mock import response, FakeResponse


class FakturoidTestCase(unittest.TestCase):

    @patch('requests.post', return_value=response("token.json"))
    def setUp(self, mock):
        self.fa = Fakturoid('myslug')
        self.fa.oauth_token_client_credentials_flow('pytest', b'client_id', b'client_secret')

class OAuthTestCase(FakturoidTestCase):
    @patch('requests.post', return_value=response('token.json'))
    def test_oauth_credentials_flow(self, mock):
        self.fa.oauth_token_client_credentials_flow('pytest', b'client_id', b'client_secret')


class AccountTestCase(FakturoidTestCase):
    @patch('requests.get', return_value=response('account.json'))
    def test_load(self, mock):
        account = self.fa.account()

        self.assertEqual('https://app.fakturoid.cz/api/v3/accounts/myslug/account.json', mock.call_args[0][0])
        self.assertEqual("Alexandr Hejsek", account.name)
        self.assertEqual("testdph@test.cz", account.email)


class SubjectTestCase(FakturoidTestCase):

    @patch('requests.get', return_value=response('subject_28.json'))
    def test_load(self, mock):
        subject = self.fa.subject(28)

        self.assertEqual('https://app.fakturoid.cz/api/v3/accounts/myslug/subjects/28.json', mock.call_args[0][0])
        self.assertEqual(28, subject.id)
        self.assertEqual('47123737', subject.registration_no)
        self.assertEqual('2012-06-02T09:34:47+02:00', subject.updated_at.isoformat())

    @patch('requests.get', return_value=response('subjects.json'))
    def test_find(self, mock):
        subjects = self.fa.subjects()

        self.assertEqual('https://app.fakturoid.cz/api/v3/accounts/myslug/subjects.json', mock.call_args[0][0])
        self.assertEqual(2, len(subjects))
        self.assertEqual('Apple Czech s.r.o.', subjects[0].name)


class InvoiceTestCase(FakturoidTestCase):

    @patch('requests.get', return_value=response('invoice_9.json'))
    def test_load(self, mock):
        invoice = self.fa.invoice(9)

        self.assertEqual('https://app.fakturoid.cz/api/v3/accounts/myslug/invoices/9.json', mock.call_args[0][0])
        self.assertEqual('2012-0004', invoice.number)

    @patch('requests.post', return_value=FakeResponse(''))
    def test_fire(self, mock):
        self.fa.fire_invoice_event(9, 'pay')

        mock.assert_called_once_with('https://app.fakturoid.cz/api/v3/accounts/myslug/invoices/9/fire.json',
                                     headers={'User-Agent': Fakturoid.user_agent,
                                              'Authorization': 'Bearer 63cfcf07492268ab0e3c58e9fa48096dc5bf0a9b7bbd2f6f45e0a6fa9fc2074a4523af3538f0df5c',
                                              'Content-Type': 'application/json'},
                                     data='{}',
                                     params={'event': 'pay'})

    @patch('requests.post', return_value=FakeResponse(''))
    def test_fire_with_args(self, mock):
        self.fa.fire_invoice_event(9, 'pay', paid_at=date(2018, 11, 19))

        mock.assert_called_once_with('https://app.fakturoid.cz/api/v3/accounts/myslug/invoices/9/fire.json',
                                     data='{}',
                                     headers={'User-Agent': Fakturoid.user_agent,
                                              'Authorization': 'Bearer 63cfcf07492268ab0e3c58e9fa48096dc5bf0a9b7bbd2f6f45e0a6fa9fc2074a4523af3538f0df5c',
                                              'Content-Type': 'application/json'},
                                     params={'event': 'pay', 'paid_at': '2018-11-19'})

    @patch('requests.get', return_value=response('invoices.json'))
    def test_find(self, mock):
        self.fa.invoices()[:10]

        self.assertEqual('https://app.fakturoid.cz/api/v3/accounts/myslug/invoices.json', mock.call_args[0][0])
        # TODO paging test


class GeneratorTestCase(FakturoidTestCase):

    @patch('requests.get', return_value=response('generator_4.json'))
    def test_load(self, mock):
        g = self.fa.generator(4)

        self.assertEqual('https://app.fakturoid.cz/api/v3/accounts/myslug/generators/4.json', mock.call_args[0][0])
        self.assertEqual('Podpora', g.name)

    @patch('requests.get', return_value=response('generators.json'))
    def test_find(self, mock):
        generators = self.fa.generators()

        self.assertEqual('https://app.fakturoid.cz/api/v3/accounts/myslug/generators.json', mock.call_args[0][0])
        self.assertEqual(2, len(generators))


if __name__ == '__main__':
    unittest.main()
