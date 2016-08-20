""" Discord REST Client """
import requests

BASE_URL = "https://discordapp.com/api/"


class Client:
    def __init__(self, token, token_type="bot"):
        if token_type == "bearer":
            prefix = "Bearer "
        else:
            prefix = "Bot "

        self._headers = {
            "Authorization": "{prefix}{token}".format(prefix=prefix, token=token)
        }

    def get_headers(self):
        return self._headers

    def get(self, path):
        resp = requests.get(
            "{}{}".format(BASE_URL, path),
            headers=self.get_headers()
        )

        return resp.json()
