from r2s.api_adaptor import APIAdaptor
from unittest.mock import Mock, patch
import pytest
from infra.data import options_api, sample_response_body
from requests import HTTPError

@patch('requests.post')
def test_auth(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'auth_token':'mock_token'}
    adaptor = APIAdaptor(options_api)

    auth_headers = adaptor.getAuthHeaders()
    assert auth_headers == {'x-api-key':options_api['api_key'], 'Authorization':'mock_token'}
    
    assert adaptor.auth_token == 'mock_token'
    assert adaptor.auth_headers['Authorization'] == 'mock_token'


@patch('requests.post')
def test_erro_auth(mock_post):
    mock_post.return_value.status_code = 403
    mock_post.return_value.json.return_value = {'status': 'ERROR','msg': 'Could not find user or wrong password.'}
    mock_post.return_value.raise_for_status.side_effect = HTTPError()
    adaptor = APIAdaptor(options_api)

    with pytest.raises(HTTPError):
        adaptor.refreshAuthToken()




@patch('requests.post')
def test_fetch_items(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = sample_response_body

    with patch.object(APIAdaptor, 'getAuthHeaders', return_value = 'mock_token') as mock_method:
        adaptor = APIAdaptor(options_api)
        response = adaptor.fetchItems('')
        assert response.json() == sample_response_body



