__author__ = 'omriariav'
import requests
import xmltodict
from pprint import pprint
import hashlib
import urllib

#CONSTS:
PRODUCTION_URL = "http://api4.liverail.com"
DEV_URL = "http://api4.int.liverail.com"



class LiveRailClass():

    def __init__(self,env="dev"):
        self._headers = {"content-type": "application/x-www-form-urlencoded"}
        if env == "dev":
            self._url = DEV_URL
        else:
            self._url = PRODUCTION_URL
        self._login_flag = False
        self._token = ""
        self._entity = ""

    def _get(self,rest_path, payload={}):
        _request_url = self._url + rest_path
        r = requests.get(_request_url, params=payload, headers=self._headers)
        return r.content

    def _post(self,rest_path, payload={}):
        res = {}
        _request_url = self._url + rest_path
        if self._token != "":
            payload['token'] = self._token
        payload = urllib.urlencode(payload)
        r = requests.post(_request_url, data=payload, headers=self._headers)
        xmlParsed = xmltodict.parse(r.content)
        pprint(xmlParsed)
        res['python_used_url'] = _request_url
        res['python_used_payload'] = payload
        res['liverailapiused'] = xmlParsed['liverailapi']['@requested']
        res['api_version'] = xmlParsed['liverailapi']['@api_version']
        if xmlParsed['liverailapi']['status'] == "fail":
            res['error'] = True
            res['error_description'] = xmlParsed['liverailapi']['error']['message']
            res['error_code'] = xmlParsed['liverailapi']['error']['code']
            if xmlParsed['liverailapi']['error'].has_key('field'):
                res['error_field'] = xmlParsed['liverailapi']['error']['field']
            res['payload'] = ""
        else:
            res['error'] = False
            res['error_description'] = None
            res['error_code'] = None
            res['error_field'] = None
            res["payload"] = xmlParsed['liverailapi']
        return res

    def login(self, username, password):
        hashedPassword = hashlib.md5(password).hexdigest()
        username = username.strip()
        res = self._post("/login", {"username": username, "password": hashedPassword})
        if res['error']:
            self._login_flag = False
            print "Login failure"
            return False
        self._token = res['payload']['auth']['token']
        self._entity = res['payload']['auth']['entity']['entity_id']
        self._login_flag = True
        return True

    def setEntity(self,entity_id):
        rest_path = "/set/entity"
        res = self._post(rest_path,{"entity_id":entity_id})
        return res


    def revenueReport(self, payload):
        rest_path = "/statistics/aggregated"
        res = self._post(rest_path, payload)
        return res
