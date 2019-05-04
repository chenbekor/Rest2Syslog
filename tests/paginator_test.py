from r2s_paginator import Paginator
from r2s_state import State, DEFAULT_PERSIST_PATH
from infra.data import *
from infra.api_mock import * 
from infra.utils import *

def test_empty_page():
    paginator = Paginator(options, api_mock())
    paginator.next()
    assert paginator.fetchPage() == None

def test_single_page():
    paginator = Paginator(options, api_mock(single_page))
    paginator.next()
    assert paginator.fetchPage() == first_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == None    


def test_no_new_records():
    paginator = Paginator(options, api_mock([first_page]), State(last_record_id='1'))
    paginator.next()
    assert paginator.fetchPage() == None
    
    paginator.next()
    assert paginator.fetchPage() == None

def test_one_item():
    paginator = Paginator(options, api_mock([first_page]), State(last_record_id='2'))
    paginator.next()
    assert paginator.fetchPage() == [{'id':'1'}]

    paginator.next()
    items = paginator.fetchPage()
    assert items == None


def test_two_pages():
    paginator = Paginator(options, api_mock(two_pages))
    
    paginator.next()
    items = paginator.fetchPage()
    assert items == first_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == second_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == None    

def test_4_items():
    paginator = Paginator(options, api_mock(two_pages), state = State(last_record_id='5'))
    
    paginator.next()
    items = paginator.fetchPage()
    assert items == first_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == [{'id':'4'}]

    paginator.next()
    items = paginator.fetchPage()
    assert items == None

def test_max_pages():
    paginator = Paginator(options_two_page, api_mock(three_pages), state = State(last_record_id='100'))
    
    paginator.next()
    items = paginator.fetchPage()
    assert items == first_page

    is_available = paginator.next()
    assert is_available == True

    items = paginator.fetchPage()
    assert items == second_page

    is_available = paginator.next()
    assert is_available == False

