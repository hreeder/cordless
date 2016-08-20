"""
    Discord Role - Guild roles
"""


class Role:
    def __init__(self, client, server, parsed_response=None):
        self.client = client
        self.server = server
        if parsed_response:
            self.id = parsed_response['id']
            self.name = parsed_response['name']
            self.hoist = parsed_response['hoist']
            self.mentionable = parsed_response['mentionable']
            self.color = parsed_response['color']
            self.permissions = parsed_response['permissions']
