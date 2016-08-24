import json
import unittest
import responses

from tests.util import get_mock_response

from cordless.client import Client
from cordless.guild import Guild


class TestGuild(unittest.TestCase):

    def setUp(self):
        self.client = Client('myToken')

    @responses.activate
    def test_construct_guild_from_json(self):
        sample = get_mock_response('guilds/get_guild')

        guild = Guild(self.client, parsed_response=sample)
        self.assertEqual(sample['id'], guild.id)
        self.assertEqual(sample['name'], guild.name)

    @responses.activate
    def test_get_guild(self):
        sample = get_mock_response('guilds/get_guild')

        responses.add(responses.GET,
                      'https://discordapp.com/api/guilds/{}'.format(sample['id']),
                      json=sample)

        guild = Guild.get(self.client, sample['id'])

        self.assertEqual(type(guild), Guild)

        self.assertEqual(sample['id'], guild.id)
        self.assertEqual(sample['name'], guild.name)
        self.assertEqual(sample['mfa_level'], guild.mfa_level)
        self.assertEqual(sample['verification_level'], guild.verification_level)
        self.assertEqual(sample['afk_timeout'], guild.afk_timeout)
        self.assertEqual(sample['region'], guild.region)
        self.assertEqual(sample['afk_channel_id'], guild.afk_channel_id)
        self.assertEqual(sample['embed_channel_id'], guild.embed_channel_id)
        self.assertEqual(sample['icon'], guild.icon)

        self.assertEqual(len(sample['roles']), len(guild.roles))

    @responses.activate
    def test_get_guild_channels(self):
        sample_guild = get_mock_response('guilds/get_guild')
        guild = Guild(self.client, parsed_response=sample_guild)

        sample_channels = get_mock_response('guilds/get_guild_channels')

        responses.add(responses.GET,
                      'https://discordapp.com/api/guilds/{}/channels'.format(guild.id),
                      json=sample_channels)

        channels = guild.get_channels()

        self.assertEqual(len(sample_channels), len(channels))

    @responses.activate
    def test_create_guild_text_channel(self):
        sample_guild = get_mock_response('guilds/get_guild')
        guild = Guild(self.client, parsed_response=sample_guild)

        sample_channel = get_mock_response('guilds/post_guild_channels')

        responses.add(responses.POST,
                      'https://discordapp.com/api/guilds/{}/channels'.format(guild.id),
                      json=sample_channel)

        new_channel = guild.create_channel(name=sample_channel['name'])
        self.assertEqual(sample_channel['name'], new_channel.name)

    @responses.activate
    def test_create_guild_role(self):
        sample_guild = get_mock_response('guilds/get_guild')
        guild = Guild(self.client, parsed_response=sample_guild)

        sample_blank = get_mock_response('guilds/post_roles')

        responses.add(responses.POST,
                      'https://discordapp.com/api/guilds/{}/roles'.format(guild.id),
                      json=sample_blank)

        new_role = guild.create_role()
        self.assertEqual(sample_blank['name'], new_role.name)

    @responses.activate
    def test_create_guild_role_with_attribs(self):
        sample_guild = get_mock_response('guilds/get_guild')
        guild = Guild(self.client, parsed_response=sample_guild)

        sample_blank = get_mock_response('guilds/post_roles')

        responses.add(responses.POST,
                      'https://discordapp.com/api/guilds/{}/roles'.format(guild.id),
                      json=sample_blank)

        def handle_modification(request):
            body = request.body.decode('utf-8')
            body = json.loads(body)
            sample_blank.update(body)
            return 200, {}, json.dumps(sample_blank)

        responses.add_callback(responses.PATCH,
                               'https://discordapp.com/api/guilds/{}/roles/{}'.format(guild.id, sample_blank['id']),
                               callback=handle_modification,
                               content_type='application/json')

        new_role = guild.create_role(name="My Role")
        self.assertEqual("My Role", new_role.name)
