"""
    Discord Channel
    {
        "permission_overwrites": []
    }
"""


class Channel:
    def __init__(self, client, parsed_response=None):
        self.client = client
        if parsed_response:
            self.id = parsed_response['id']
            self.name = parsed_response['name']
            self.position = parsed_response['position']
            self.type = parsed_response['type']
            self.private = parsed_response['is_private']

            if "guild_id" in parsed_response:
                self.guild_id = parsed_response['guild_id']
            else:
                self.guild_id = None

            if self.type == "text":
                self.topic = parsed_response['topic']
                self.last_message_id = parsed_response['last_message_id']
            else:
                self.bitrate = parsed_response['bitrate']
                self.user_limit = parsed_response['user_limit']
