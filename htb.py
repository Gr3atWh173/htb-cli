"""
A wrapper around the Hack the Box API
"""
import requests

class HTBAPIError(Exception):
    """Raised when API fails"""
    pass

class HTB:
    """
    Hack the Box API Wrapper

    :attr api_key: API Key used for authenticated queries
    """

    BASE_URL = 'https://www.hackthebox.eu/api'

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def _validate_response(response):
        """
        Validate the response from the API

        :params response: the response dict received from an API call
        :returns: the response dict if the call was successfull
        """
        if response['success'] != '1':
            raise HTBAPIError("success != 1")
        return response

    @classmethod
    def _get(cls, path: str) -> dict:
        """
        Helper function to get an API endpoint and validate the response

        :params cls: the HTB class
        :params path: the path to get including leading forward slash
        :returns: the response dict from the endpoint
        """
        return HTB._validate_response(requests.get(cls.BASE_URL + path).json())

    @classmethod
    def _post(cls, path: str, data: dict = None) -> dict:
        """
        Helper function to get an API endpoint and validate the response

        :params cls: the HTB class
        :params path: the path to get including leading forward slash
        :returns: the response dict from the endpoint
        """
        return HTB._validate_response(requests.post(cls.BASE_URL + path, data=data).json())

    def _auth(self, path: str) -> str:
        """
        Helper function to generate an authenticated URL

        :params self: HTB object in use
        :params path: string containing path to query
        :returns: path to authenticated query
        """
        return "{}?api_token={}".format(path, self.api_key)

    @classmethod
    def global_stats(cls) -> dict:
        """
        Returns current stats about Hack the Box

        :params cls: the HTB class
        :returns: global stats dict
        """
        return cls._post('/stats/global')

    @classmethod
    def overview_stats(cls) -> dict:
        """
        Returns overview stats about Hack the Box

        Doesn't include success key

        :params cls: the HTB class
        :returns: overview stats dict
        """
        return requests.get(cls.BASE_URL + '/stats/overview').json()

    @classmethod
    def daily_owns(cls, count: int = 30) -> dict:
        """
        Returns the number of owns and total number of users after the last COUNT days

        :params cls: the HTB class
        :params count: the number of days to get data from
        :returns: daily owns dict
        """
        return cls._post('/stats/daily/owns/{}'.format(count))

    def list_conversations(self) -> dict:
        """
        Return the conversations dict

        Doesn't include success key

        :params self: HTB object in use
        :returns: conversations dict
        """
        return requests.post(self.BASE_URL + self._auth('/conversations/list/')).json()

    def vpn_freeslots(self) -> dict:
        """
        Return information about free slots on the VPN

        :params self: HTB object in use
        :returns: vpn_freeslots dict
        """
        return self._post(self._auth('/vpnserver/freeslots/'))

    def vpn_statusall(self) -> dict:
        """
        Return information about the status of every VPN

        :params self: HTB object in use
        :returns: vpn_statusall dict
        """
        return self._get(self._auth('/vpnserver/status/all/'))

    def connection_status(self) -> dict:
        """
        Return connection status information

        Success key seems to be behaving incorrectly

        :params self: HTB object in use
        :returns: connection_status dict
        """
        return requests.post(self.BASE_URL + self._auth('/users/htb/connection/status/')).json()

    def fortress_connection_status(self) -> dict:
        """
        Return fortress connection status information

        Success key seems to be behaving incorrectly

        :params self: HTB object in use
        :returns: fortress_connection_status dict
        """
        return requests.post(self.BASE_URL + self._auth('/users/htb/fortress/connection/status/')).json()

    def switch_vpn(self, lab: str) -> dict:
        """
        Switch the VPN your profile is connected to

        Success key doesn't exist

        :params self: HTB object in use
        :params lab: the lab to connect to, either free, usvip or euvip
        :returns: switch_vpn dict
        """

        if lab not in ("usfree", "eufree", "usvip", "euvip"):
            raise HTBAPIError("invalid lab")
        else:
            return requests.post(self.BASE_URL + self._auth('/labs/switch/{}/'.format(lab))).json()

    def get_machines(self) -> dict:
        """
        Get all machines on the network

        :params self: HTB object in use
        :returns: machines dict
        """
        return requests.get(self.BASE_URL + self._auth('/machines/get/all/')).json()

    def get_machine(self, mid: int) -> dict:
        """
        Get a single machine on the network

        :params self: HTB object in use
        :params mid: Machine ID
        :returns: machine dict
        """
        return requests.get(self.BASE_URL + self._auth('/machines/get/{}/'.format(mid))).json()

    def own_machine_user(self, mid: int, hsh: str, diff: int) -> bool:
        """
        Own a user challenge on a machine

        :params self: HTB object in use
        :params mid: Machine ID
        :params hsh: User Hash
        :params diff: difficult (10-100)
        :returns: bool if successful
        """
        try:
            self._post(self._auth('/machines/own/user/{}/'.format(mid)),
                       {"hash": hsh, "diff": diff})
            return True
        except HTBAPIError:
            return False

    def own_machine_root(self, mid: int, hsh: str, diff: int) -> bool:
        """
        Own a root challenge on a machine

        :params self: HTB object in use
        :params mid: Machine ID
        :params hsh: Root Hash
        :params diff: difficult (10-100)
        :returns: bool if successful
        """
        try:
            self._post(self._auth('/machines/own/root/{}/'.format(mid)),
                       {"hash": hsh, "diff": diff})
            return True
        except HTBAPIError:
            return False

    def reset_machine(self, mid: int) -> dict:
        """
        Reset a machine on the network

        :params self: HTB object in use
        :params mid: Machine ID
        :returns: reset_machine dict
        """
        return self._post(self._auth('/vm/reset/{}/'.format(mid)))
