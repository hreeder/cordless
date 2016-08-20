import unittest
import responses

from tests.util import get_mock_response

from cordless.client import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        self.token = "demoTOKEN"
        self.client = Client(self.token)

    def test_token_default_type_bot(self):
        expected = "Bot {}".format(self.token)
        actual = self.client.get_headers()['Authorization']

        self.assertEqual(expected, actual)

    def test_token_type_oauth(self):
        client = Client(self.token, token_type="bearer")

        expected = "Bearer {}".format(self.token)
        actual = client.get_headers()['Authorization']

        self.assertEqual(expected, actual)

    @responses.activate
    def test_get_wrapper(self):
        mock = get_mock_response('gateway')
        responses.add(responses.GET,
                      "https://discordapp.com/api/gateway",
                      json=mock)
        response = self.client.get('gateway')

        self.assertEqual(mock, response)
        self.assertEqual(1, len(responses.calls))

        self.assertEqual("Bot {}".format(self.token),
                         responses.calls[0].request.headers['Authorization'])
