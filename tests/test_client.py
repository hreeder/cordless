import json
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

    @responses.activate
    def test_patch_wrapper(self):
        def request_callback(request):
            before = get_mock_response('guilds/get_guild')
            body = request.body.decode('utf-8')
            body = json.loads(body)
            before.update(body)
            return 200, {}, json.dumps(before)

        responses.add_callback(responses.PATCH,
                               "https://discordapp.com/api/sample",
                               callback=request_callback,
                               content_type='application/json')

        data = {
            "name": "Test Name"
        }

        response = self.client.patch('sample', data)

        self.assertEqual(data['name'], response['name'])
        self.assertEqual(1, len(responses.calls))

        for key, value in data.items():
            self.assertEqual(value, response[key])

        self.assertEqual("Bot {}".format(self.token),
                         responses.calls[0].request.headers['Authorization'])

    @responses.activate
    def test_post_wrapper(self):
        def request_callback(request):
            return 200, {}, request.body.decode('utf-8')
        responses.add_callback(responses.POST,
                               "https://discordapp.com/api/sample",
                               callback=request_callback,
                               content_type='application/json')

        data = {
            "name": "Test Name"
        }

        response = self.client.post('sample', data)

        self.assertEqual(data['name'], response['name'])
        self.assertEqual(1, len(responses.calls))

        self.assertEqual("Bot {}".format(self.token),
                         responses.calls[0].request.headers['Authorization'])
