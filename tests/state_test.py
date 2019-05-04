from r2s_state import State
from r2s_paginator import Paginator

from infra.data import *
from infra.api_mock import *
from infra.utils import *


def  test_persist():
    state = State(last_record_id='4')
    assert state.last_record_id == '4'

    state.last_record_id = '6'
    state.persist()

    restored_state = State()

    assert restored_state.last_record_id == '6'

def test_state_based_pagination():
    state = State()
    assert state.last_record_id == ''

    mocker = api_mock([first_page])
    paginator = Paginator(options, mocker, state)
    
    paginator.next()
    items = paginator.fetchPage()
    assert items == first_page

    mocker.setPages([second_page,first_page])
    paginator.reset()

    paginator.next()
    items = paginator.fetchPage()
    assert items == second_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == None
    
    mocker.setPages([fourth_page, third_page, second_page,first_page])
    paginator.reset()

    paginator.next()
    items = paginator.fetchPage()
    assert items == fourth_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == third_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == None

    mocker.setPages([fourth_page])
    paginator.reset()

    paginator.next()
    items = paginator.fetchPage()
    assert items == None

def test_pagination_after_service_restart():
    state = State()
    mocker = api_mock([second_page,first_page])
    paginator = Paginator(options, mocker, state)
    paginator.next()
    #fetch second page
    items = paginator.fetchPage()
    #fetch first page
    items = paginator.fetchPage()
    #persist
    paginator.reset()

    #restart opertion
    state = State()
    mocker = api_mock([fourth_page, third_page, second_page,first_page])
    paginator = Paginator(options, mocker, state)

    paginator.next()
    items = paginator.fetchPage()
    assert items == fourth_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == third_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == None    