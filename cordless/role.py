"""
    Discord Role - Guild roles
"""


class Role:
    def __init__(self, client, server, parsed_response=None):
        self.client = client
        self.server = server
        if parsed_response:
            self._parse_response(parsed_response)

    def _parse_response(self, parsed_response):
        self.id = parsed_response['id']
        self.name = parsed_response['name']
        self.hoist = parsed_response['hoist']
        self.mentionable = parsed_response['mentionable']
        self.color = parsed_response['color']
        self.permissions = parsed_response['permissions']

    def update(self, **kwargs):
        response = self.client.patch("guilds/{}/roles/{}".format(self.server.id, self.id), kwargs)
        self._parse_response(response)