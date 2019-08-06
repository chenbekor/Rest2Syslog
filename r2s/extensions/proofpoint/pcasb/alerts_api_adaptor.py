from r2s.utils import _print,_print_error
import requests
from r2s.extensions.abstract import R2SAPIAdaptor

class PCASBAlertsAPIAdaptor(R2SAPIAdaptor):
    def __init__(self,options):
        _print("About to initialize PCASBAlertsAPIAdaptor...")
        self.auth_url = options['auth_url']
        self.alerts_url = options['alerts_url']
        self.auth_headers = {'x-api-key':options['api_key'], 'Authorization':''}
        self.auth_body = {'client_id':options['client_id'],'client_secret':options['client_secret']}
        self.auth_token = None
        super().__init__()

    def getAuthHeaders(self):
        if self.auth_token is None:
            self.refreshAuthToken()
        return self.auth_headers
    
    def refreshAuthToken(self):
        _print("building auth request")
        r = requests.post(self.auth_url,json=self.auth_body, headers=self.auth_headers)
        _print("Auth request executed")
        if r.status_code != 200 :
            _print_error('Got non 200 response code: ' + str(r.status_code))
            _print_error('Response body: ' + r.text)
            r.raise_for_status()
        self.auth_token = r.json()['auth_token']
        _print('Access Token was refreshed successfully.')
        self.auth_headers['Authorization'] = self.auth_token

    def buildRequestBody(self, page_num):
        return {'page':page_num}

    def handleResponseError(self,response):
        _print('Got non 200 response code')
        if response.status_code == 401:
            _print('The Auth Token was probably expired.')
            self.auth_token = None
        else:
            _print_error('Error Response code: ' + str(response.status_code))
            _print_error('Error Response body: ' + response.text)

    def fetchItems(self, page_num):
        headers = self.getAuthHeaders()
        request_body = self.buildRequestBody(page_num)
        is_content_available = False
        try:
            response = requests.post(self.alerts_url,json = request_body, headers = headers)
            _print('Fetch Page ' + str(page_num) + ' executed')
            if response.status_code != 200:                
                self.handleResponseError(response)
                return None
            else:
                is_content_available = True
                return response.json()['alerts']
                #r'''..'''
        except Exception as ex:
            _print_error('Error while trying to fetch items.')
            _print_error(ex)
            if is_content_available:
                _print('response.json() failed for the following payload: {}'.format(response.text))
            return None
