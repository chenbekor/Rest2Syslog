import requests
from r2s_utils import _print

class Paginator:
    def __init__(self,options):
        self.is_reached_last = False
        self.page_num = 0
        self.auth_url = options['auth_url']
        self.alerts_url = options['alerts_url']
        self.auth_headers = {'x-api-key':options['api_key'], 'Authorization':''}
        self.auth_body = {'client_id':options['client_id'],'client_secret':options['client_secret']}
        self.auth_token = None

    def reset(self):
        self.page_num = 0
        self.is_reached_last = False

    def getPage(self):
        return {'page':self.page_num}

    def next(self):
        self.page_num += 1


    def getAuthHeaders(self):
        if self.auth_token is None:
            self.refreshAuthToken()
        return self.auth_headers

    def refreshAuthToken(self):
        _print("building auth request")
        r = requests.post(self.auth_url,json=self.auth_body, headers=self.auth_headers)
        _print("Auth request executed")
        if r.status_code != 200 :
            _print('Got non 200 response code: ' + str(r.status_code))
            _print('Response body: ' + r.text)
            r.raise_for_status()
        self.auth_token = r.json()['auth_token']
        _print('Access Token was refreshed successfully.')
        self.auth_headers['Authorization'] = self.auth_token

    def handlePageError(self,r):
        _print('Got non 200 response code')
        if r.status_code == 401:
            _print('The Auth Token was probably expired.')
            self.auth_token = None
        else:
            _print('Error Response code: ' + str(r.status_code))
            _print('Error Response body: ' + r.text)


    def fetchPage(self):
        headers = self.getAuthHeaders()
        json = self.getPage()
        r = requests.post(self.alerts_url,json = json, headers = headers)
        _print('Fetch Page executed')
        if r.status_code != 200:
            self.handlePageError(r)
            return None
        else:
            return r.json()['alerts']
