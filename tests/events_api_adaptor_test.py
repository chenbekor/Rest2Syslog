from r2s.extensions.proofpoint.pcasb.events_api_adaptor import PCASBEventsAPIAdaptor
from unittest.mock import Mock, patch
import pytest
from infra.events_data import options_api, items, sample_response_body
from requests import HTTPError
from urllib3.exceptions import NewConnectionError

@patch('requests.post')
def test_auth(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'auth_token':'mock_token'}
    adaptor = PCASBEventsAPIAdaptor(options_api)

    auth_headers = adaptor.getAuthHeaders()
    assert auth_headers == {'x-api-key':options_api['api_key'], 'Authorization':'mock_token'}
    
    assert adaptor.auth_token == 'mock_token'
    assert adaptor.auth_headers['Authorization'] == 'mock_token'


@patch('requests.post')
def test_erro_auth(mock_post):
    mock_post.return_value.status_code = 403
    mock_post.return_value.json.return_value = {'status': 'ERROR','msg': 'Could not find user or wrong password.'}
    mock_post.return_value.raise_for_status.side_effect = HTTPError()
    adaptor = PCASBEventsAPIAdaptor(options_api)

    with pytest.raises(HTTPError):
        adaptor.refreshAuthToken()




@patch('requests.get')
def test_fetch_items(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = sample_response_body

    with patch.object(PCASBEventsAPIAdaptor, 'getAuthHeaders', return_value = 'mock_token') as mock_method:
        adaptor = PCASBEventsAPIAdaptor(options_api)
        response = adaptor.fetchItems('blabla')
        assert response["content"] == items

@patch('requests.get')
def test_fetch_items_exception(mock_get):
    mock_get.side_effect = Exception('mock connection error')

    with patch.object(PCASBEventsAPIAdaptor, 'getAuthHeaders', return_value = 'mock_token') as mock_method:
        adaptor = PCASBEventsAPIAdaptor(options_api)
        response = adaptor.fetchItems('blabla')
        assert response == None



