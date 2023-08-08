"""
## Description
Couple of helper functions.
"""
import http.client
import json
import re
from typing import Any, Dict, Optional


def ord(n: int) -> str:
    """
    Prefix numbers with their order.

    >>> from civi_core.helpers import ord
    >>> ord(13)
    '13th'
    >>> ord(22)
    '22nd'
    """
    return str(n) + (
        'th'
        if 4 <= n % 100 <= 20
        else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    )



# FIXME(gaytomycode): A request handler that works, should improve it thou to our
# needs
GET: str = 'GET'
POST: str = 'POST'

STATUS_CODE: Dict[int, str] = {}


class Request:
    """
    temporary to make api requset, it should tie into aws tools when deployed to production

    >>> request = Request(url='https://example.com', path='/v1/reservation/upcoming/', method='GET', headers={}, json={})
    >>> request.set_auth_header('Bearer ...')
    >>> response = request.send()
    >>> response.status
    >>> response.json
    """

    def __init__(
        self,
        url: str,
        path: str,
        method: str = GET,
        headers: dict[str, str] = {},
        json: dict[str, Any] = {},
    ):
        self.__url = url
        self.__path = path
        self.__method = method
        self.__headers = {
            **headers,
            'accept': '*/*',
            'Content-Type': 'application/json',
        }
        self.__req_json = json

    def send(self):
        conn = http.client.HTTPSConnection(self.__url)
        conn.request(
            self.__method,
            self.__path,
            json.dumps(self.__req_json),
            headers=self.__headers,
        )
        resp = conn.getresponse()
        if resp.status // 100 != 2:
            # FIXME(gaytomycode): raising an error here is stupid ik this is a
            # tmp class (azon?)
            raise ValueError(f'{resp.status} {resp.reason} {resp.read()}')
        return {
            'status': resp.status,
            'json': json.loads(resp.read()),
        }

    def set_auth_header(self, value):
        self.__headers['Authorization'] = value
