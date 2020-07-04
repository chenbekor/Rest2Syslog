from r2s.extensions.proofpoint.pcasb.events_paginator import PCASBEventsPaginator as Paginator
from r2s.state import State, DEFAULT_PERSIST_PATH
from infra.events_data import *
from infra.api_mock import * 
from infra.utils import *

from unittest.mock import Mock, patch
import pytest

def test_empty_page():
    paginator = Paginator(options = options, api_adaptor= api_mock())
    assert unwrap(paginator.fetchPageItems()) == None

def test_single_page():
    paginator = Paginator(options = options, api_adaptor = api_mock(single_page))
    assert unwrap(paginator.fetchPageItems()) == first_page["content"]
    items = unwrap(paginator.fetchPageItems())
    assert items == None    


def test_no_new_items():
    paginator = Paginator(options = options, api_adaptor = api_mock([empty_page]), state = State(value='BLABLA'))
    assert unwrap(paginator.fetchPageItems()) == None
    assert unwrap(paginator.fetchPageItems()) == None

def test_two_pages():
    paginator = Paginator(options = options, api_adaptor = api_mock(two_pages))
    
    items = unwrap(paginator.fetchPageItems())
    assert items == first_page["content"]

    items = unwrap(paginator.fetchPageItems())
    assert items == second_page["content"]

    items = unwrap(paginator.fetchPageItems())
    assert items == None    


def test_no_api_adaptor():
    paginator = Paginator(options = {**options,**options_api}, api_adaptor = None)
    assert paginator.api_adaptor is not None

@patch('r2s.extensions.proofpoint.pcasb.events_api_adaptor.PCASBEventsAPIAdaptor')
def test_auth_expires(api_mock):
    api_mock.fetchItems.return_value.status_code = 401
    paginator = Paginator(options = {**options,**options_api}, api_adaptor= api_mock)
    items = paginator.fetchPageItems()
    assert items == None

@patch('r2s.extensions.proofpoint.pcasb.events_api_adaptor.PCASBEventsAPIAdaptor')
def test_bad_fetch_response(api_mock):
    api_mock.fetchItems.return_value.status_code = 500
    paginator = Paginator(options = {**options,**options_api}, api_adaptor= api_mock)

    items = paginator.fetchPageItems()
    assert items == None

@patch('r2s.extensions.proofpoint.pcasb.events_api_adaptor.PCASBEventsAPIAdaptor')
def test_mallformed_response(api_mock):
    api_mock.fetchItems.return_value.status_code = 200
    api_mock.fetchItems.return_value.json.return_value = {'invalid':'boom!'}
    paginator = Paginator(options = {**options,**options_api}, api_adaptor= api_mock)

    items = paginator.fetchPageItems()
    assert items == None    