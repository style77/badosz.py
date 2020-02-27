import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

from utils import File

_executor = ThreadPoolExecutor(10)

class WrongToken(Exception):
    pass
class WrongEndpoint(Exception):
    pass
class NotEnoughParameters(Exception):
    pass


async def get_image(self, image):
    headers = image.headers
    r = await image.read()
    return File(r, headers)


class Badosz:
    API_LINK = "https://api.badosz.com"

    TO_CUT = ['?text=<text>', '?url=<url>&hex=<hex>', '?url=<url>', '?hex=<hex>']

    RAW_ENDPOINT = [endpoint.replace('GET ', '') for endpoint in requests.get(API_LINK).json()['endpoints']]
    RAW_ENDPOINT_MAP = dict()
    ENDPOINTS = list()

    for endpoint in RAW_ENDPOINT:
        for cut in TO_CUT:
            if cut in endpoint:
                if endpoint not in ENDPOINTS:
                    endpoint = endpoint.replace(cut, '')
                    ENDPOINTS.append(endpoint)

    ENDPOINTS_WITHOUT_ARGS = []
    for endpoint in RAW_ENDPOINT:
        if endpoint not in ENDPOINTS:
            t = True
            for cut in TO_CUT:
                if cut in endpoint:
                    t = False
            if t:
                ENDPOINTS_WITHOUT_ARGS.append(endpoint)

    ENDPOINTS.extend(ENDPOINTS_WITHOUT_ARGS)

    for key in ENDPOINTS:
        for value in RAW_ENDPOINT:
            if value.startswith(key):
                RAW_ENDPOINT_MAP[key] = value
            else:
                continue

    RAW_ENDPOINT_MAP['/color'] = '/color?hex=<hex>'

    def __init__(self, token, async_=False):
        self.token = token

        self.async_ = async_

        self.NSFW_ENDPOINTS = list()

    def _call_func(self, function, *args):
        if self.async_:

            async def in_thread(func):
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(_executor, func, args)

            return in_thread(function)
        else:
            return function(args)

    def init_nsfw(self):
        try:
            NSFW_ENDPOINTS = self.NSFW_ENDPOINTS = [e for e in self.endpoints['NSFWendpoints']]

            for e in NSFW_ENDPOINTS:
                self.RAW_ENDPOINT_MAP['/' + e] = '/' + e

        except Exception as e:
            print(e)
            return False
        finally:
            return True

    def _url_check(self, url):  # todo use
        return requests.head(url).status_code == 200

    def __getattr__(self, item):
        i = f"/{item}"

        if i not in self.ENDPOINTS_WITHOUT_ARGS and item not in self.NSFW_ENDPOINTS:
            raise WrongEndpoint("This endpoint doesn't exist. Or you have not initialized NSFW endpoints.")

        resp = self._call_func(self.request, i)
        return resp

    def _format(self, endpoint, args):
        if isinstance(endpoint, str):
            endpoint = endpoint
        else:
            endpoint = endpoint[0]

        e = f"{endpoint}"
        # if e not in self.ENDPOINTS:
        #     raise WrongEndpoint("This endpoint doesn't exist.")

        r_endpoint = self.RAW_ENDPOINT_MAP[endpoint]

        # if not r_endpoint:
        #     raise WrongEndpoint("This endpoint doesn't exist.")

        final_uri = ""

        if '?url=<url>&hex=<hex>' in r_endpoint:
            if len(args) < 2:
                raise NotEnoughParameters("You have to pass 2 parameters for this endpoint.")
            final_uri = r_endpoint.replace('<url>', args[0])
            final_uri = final_uri.replace('<hex>', args[1])

        elif '?text=<text>' in r_endpoint:
            if len(args) < 1:
                raise NotEnoughParameters("You have to pass 1 parameter for this endpoint.")

            final_uri = r_endpoint.replace('<text>', args[0])
        elif '?url=<url>' in r_endpoint:
            if len(args) < 1:
                raise NotEnoughParameters("You have to pass 1 parameter for this endpoint.")
            final_uri = r_endpoint.replace('<url>', args[0])
        elif '?hex=<hex>' in r_endpoint:
            if len(args) < 1:
                raise NotEnoughParameters("You have to pass 1 parameter for this endpoint.")
            final_uri = r_endpoint.replace('<hex>', args[0])
        else:
            return endpoint

        return final_uri

    def request(self, endpoint, *args, file=False, filename=None):
        try:
            if args[0] and isinstance(args[0], set):
                args = args[0]
        except Exception as e:
            pass

        url = self.API_LINK + self._format(endpoint, args)

        headers = {'Authorization': self.token}

        if self.async_:
            session = aiohttp.ClientSession()

            loop = asyncio.get_event_loop()

            response = loop.run_until_complete(session.get(url, headers=headers))
            if file:
                return File(loop.run_until_complete(response.read()), response.headers, filename=filename)
            return loop.run_until_complete(response.json())
        else:
            response = requests.get(url, headers=headers)
            if file:
                return File(response.content, response.headers, filename=filename)
            return response.json()

    def base64(self, text, *, fn="nothing"): return self.request('/base64', text, filename=fn)
    def binary(self, text, *, fn="nothing"): return self.request('/binary', text, filename=fn)
    def blurple(self, url, *, fn="nothing"): return self.request('/blurple', url, filename=fn)  # check url
    def changemymind(self, text, *, fn="nothing"): return self.request('/changemymind', text, file=True, filename=fn)
    def color(self, hex_, *, fn="nothing"): return self.request('/color', hex_, filename=fn)  # add hex checker
    def colorify(self, url, hex_, *, fn="nothing"): return self.request('/binary', (url, hex_), file=True, filename=fn)  # check url
    def decodebase64(self, text, *, fn="nothing"): return self.request('/decode-base64', text, filename=fn)
    def decodehex(self, text, *, fn="nothing"): return self.request('/decode-hex', text, filename=fn)
    def excuseme(self, text, *, fn="nothing"): return self.request('/excuseme', text, file=True, filename=fn)
    def flip(self, text, *, fn="nothing"): return self.request('/flip', text, filename=fn)
    def hex(self, text, *, fn="nothing"): return self.request('/hex', text, filename=fn)
    def invert(self, url, *, fn="nothing"): return self.request('/invert', url, file=True, filename=fn)  # check url
    def morse(self, text, *, fn="nothing"): return self.request('/morse', text, filename=fn)
    def reverse(self, text, *, fn="nothing"): return self.request('/reverse', text, filename=fn)
    def trump(self, text, *, fn="nothing"): return self.request('/trump', text, file=True, filename=fn)
    def vaporwave(self, text, *, fn="nothing"): return self.request('/vaporwave', text, file=True, filename=fn)
    def wanted(self, url, *, fn="nothing"): return self.request('/wanted', url, file=True, filename=fn)  # check url
    def wasted(self, url, *, fn="nothing"): return self.request('/wasted', url, file=True, filename=fn)  # check url


