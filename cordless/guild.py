""" Discord Guild """
from cordless.channel import Channel
from cordless.role import Role


class Guild:
    """
        Represents a Discord Guild (or Server)
    """
    def __init__(self, client, parsed_response=None):
        self.client = client
        if parsed_response:
            self.id = parsed_response['id']
            self.name = parsed_response['name']
            self.mfa_level = parsed_response['mfa_level']
            self.verification_level = parsed_response['verification_level']
            self.afk_timeout = parsed_response['afk_timeout']
            self.region = parsed_response['region']
            self.afk_channel_id = parsed_response['afk_channel_id']
            self.embed_channel_id = parsed_response['embed_channel_id']
            self.icon = parsed_response['icon']
            self.roles = [Role(client, self, parsed_response=role) for role in parsed_response['roles']]

    @classmethod
    def get(cls, client, guild_id):
        returned = client.get("guilds/{}".format(guild_id))
        return Guild(client, parsed_response=returned)

    def get_channels(self):
        returned = self.client.get("guilds/{}/channels".format(self.id))
        return [Channel(self.client, parsed_response=channel) for channel in returned]

    def create_channel(self, **kwargs):
        returned = self.client.post("guilds/{}/channels".format(self.id), kwargs)
        return Channel(self.client, parsed_response=returned)

    def create_role(self, **kwargs):
        returned = self.client.post("guilds/{}/roles".format(self.id))
        role = Role(self.client, self, parsed_response=returned)

        if kwargs:
            role.update(**kwargs)

        return role
