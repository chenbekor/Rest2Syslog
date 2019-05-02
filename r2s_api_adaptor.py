from r2s_utils import _print
import requests

class APIAdaptor:
    def __init__(self,options):
        self.auth_url = options['auth_url']
        self.alerts_url = options['alerts_url']
        self.auth_headers = {'x-api-key':options['api_key'], 'Authorization':''}
        self.auth_body = {'client_id':options['client_id'],'client_secret':options['client_secret']}
        self.auth_token = None

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

    def executeRequest(self, page):
        headers = self.getAuthHeaders()
        r = requests.post(self.alerts_url,json = page, headers = headers)
        _print('Fetch Page executed')
        return r