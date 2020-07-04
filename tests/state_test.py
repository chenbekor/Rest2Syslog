from r2s.state import State
from r2s.extensions.proofpoint.pcasb.alerts_paginator import PCASBAlertsPaginator as Paginator

from infra.data import *
from infra.api_mock import *
from infra.utils import *

def  test_persist():
    state = State(value='4')
    state.persist() #store ro disk

    restored_state = State() #loads from disk
    assert restored_state.value == '4'

    restored_state.setValue('6') #also persist

    restored_second_state = State() #loads from disk

    assert restored_second_state.value == '6'

def test_persist_invalid_path():
    state = State(value='4',persist_path='/invalid_path/')
    state.persist() #should persist to disk but fails due to bad path

    restored_state = State(persist_path='/invalid_path/') #loads from disk
    assert restored_state.value == ''  #value lost - due to invalid persist path

def test_state_based_pagination():
    state = State(value=0)
    assert state.value == 0

    mocker = api_mock([first_page])
    paginator = Paginator(options = options, api_adaptor= mocker, state = state)
    
    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == first_page

    mocker.setPages([second_page,first_page])
    paginator.reset()

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == second_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None
    
    mocker.setPages([fourth_page, third_page, second_page,first_page])
    paginator.reset()

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == fourth_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == third_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None

    mocker.setPages([fourth_page])
    paginator.reset()

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None

def test_pagination_after_service_restart():
    mocker = api_mock([second_page,first_page])
    paginator = Paginator(options = options, api_adaptor= mocker)
    paginator.next()
    #fetch second page
    items = unwrap(paginator.fetchPageItems())
    #fetch first page
    items = unwrap(paginator.fetchPageItems())
    #persist
    paginator.reset()

    #restart opertion => new paginator
    mocker = api_mock([third_page + second_page,first_page])
    paginator = Paginator(options = options, api_adaptor = mocker)

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == third_page  #only new items from page three should appear

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None