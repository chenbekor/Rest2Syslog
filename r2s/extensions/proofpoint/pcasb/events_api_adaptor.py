from r2s.utils import _print,_print_error
import requests
from r2s.extensions.abstract import R2SAPIAdaptor
from datetime import date, timedelta

class PCASBEventsAPIAdaptor(R2SAPIAdaptor):
    def __init__(self,options):
        _print("About to initialize PCASBEventsAPIAdaptor...")
        self.auth_url = options['auth_url']
        self.events_url = options['events_url']
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

    def buildRequestURL(self, next_page_token):
        if not next_page_token:
            return '{}nextPage={}'.format(self.events_url,next_page_token)
        else:
            dt = date.today() - timedelta(1)
            url = '{}startTime={}'.format(self.events_url,dt)
            _print('empty next_page_token, fetching all events since {} using this URL: {}'.format(dt, url))
            return url


    def handleResponseError(self,response):
        _print('Got non 200 response code')
        if response.status_code == 401:
            _print('The Auth Token was probably expired.')
            self.auth_token = None
        else:
            _print_error('Error Response code: ' + str(response.status_code))
            _print_error('Error Response body: ' + response.text)

    def fetchItems(self, next_page_token):
        headers = self.getAuthHeaders()
        request_url = self.buildRequestURL(next_page_token)
        is_content_available = False
        try:
            response = requests.get(request_url, headers = headers)
            _print('Fetch Page ' + str(next_page_token) + ' executed')
            if response.status_code != 200:                
                self.handleResponseError(response)
                return None
            else:
                is_content_available = True
                return response.json()
                #r'''..'''
        except Exception as ex:
            _print_error('Error while trying to fetch events.')
            _print_error(ex)
            if is_content_available:
                _print('response.json() failed for the following payload: {}'.format(response.text))
            return None
