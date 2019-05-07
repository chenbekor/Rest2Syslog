from r2s.paginator import Paginator
from r2s.state import State, DEFAULT_PERSIST_PATH
from infra.data import *
from infra.api_mock import * 
from infra.utils import *

from unittest.mock import Mock, patch
import pytest

def test_empty_page():
    paginator = Paginator(options, api_mock())
    paginator.next()
    assert unwrap(paginator.fetchPageItems()) == None

def test_single_page():
    paginator = Paginator(options, api_mock(single_page))
    paginator.next()
    assert unwrap(paginator.fetchPageItems()) == first_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None    


def test_no_new_items():
    paginator = Paginator(options, api_mock([first_page]), State(last_item_id='1'))
    paginator.next()
    assert unwrap(paginator.fetchPageItems()) == None
    
    paginator.next()
    assert unwrap(paginator.fetchPageItems()) == None

def test_one_item():
    paginator = Paginator(options, api_mock([first_page]), State(last_item_id='2'))
    paginator.next()
    assert unwrap(paginator.fetchPageItems()) == [{'id':'1'}]

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None


def test_two_pages():
    paginator = Paginator(options, api_mock(two_pages))
    
    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == first_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == second_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None    

def test_4_items():
    paginator = Paginator(options, api_mock(two_pages), state = State(last_item_id='5'))
    
    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == first_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == [{'id':'4'}]

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None

def test_max_pages():
    paginator = Paginator({**options,**options_two_page}, api_mock(three_pages), state = State(last_item_id='100'))
    
    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == first_page

    is_available = paginator.next()
    assert is_available == True

    items = unwrap(paginator.fetchPageItems())
    assert items == second_page

    is_available = paginator.next()
    assert is_available == False

def test_no_max_pages():
    with pytest.raises(KeyError):
        paginator = Paginator(options = {})

def test_no_api_adaptor():
    paginator = Paginator(options = {**options,**options_api}, api_adaptor = None)
    assert paginator.api_adaptor is not None

@patch('r2s.extensions.proofpoint.pcasb.alerts_api_adaptor.PCASBAlertsAPIAdaptor')
def test_auth_expires(api_mock):
    api_mock.fetchItems.return_value.status_code = 401
    paginator = Paginator(options = {**options,**options_api}, api_adaptor= api_mock)
    items = paginator.fetchPageItems()
    assert items == None

@patch('r2s.extensions.proofpoint.pcasb.alerts_api_adaptor.PCASBAlertsAPIAdaptor')
def test_bad_fetch_response(api_mock):
    api_mock.fetchItems.return_value.status_code = 500
    paginator = Paginator(options = {**options,**options_api}, api_adaptor= api_mock)

    items = paginator.fetchPageItems()
    assert items == None

@patch('r2s.extensions.proofpoint.pcasb.alerts_api_adaptor.PCASBAlertsAPIAdaptor')
def test_mallformed_response(api_mock):
    api_mock.fetchItems.return_value.status_code = 200
    api_mock.fetchItems.return_value.json.return_value = {'invalid':'boom!'}
    paginator = Paginator(options = {**options,**options_api}, api_adaptor= api_mock)

    items = paginator.fetchPageItems()
    assert items == None    