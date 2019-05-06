from r2s.state import State
from r2s.paginator import Paginator

from infra.data import *
from infra.api_mock import *
from infra.utils import *

def  test_persist():
    state = State(last_item_id='4')
    state.persist() #store ro disk

    restored_state = State() #loads from disk
    assert restored_state.last_item_id == '4'

    restored_state.setLastItemId('6') #also persist

    restored_second_state = State() #loads from disk

    assert restored_second_state.last_item_id == '6'

def test_persist_invalid_path():
    state = State(last_item_id='4',persit_path='/invalid_path/mock.obj')
    state.persist() #should persist to disk but fails due to bad path

    restored_state = State() #loads from disk
    assert restored_state.last_item_id == ''  #value lost - due to invalid persist path

def test_state_based_pagination():
    state = State()
    assert state.last_item_id == ''

    mocker = api_mock([first_page])
    paginator = Paginator(options, mocker, state)
    
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
    state = State()
    mocker = api_mock([second_page,first_page])
    paginator = Paginator(options, mocker, state)
    paginator.next()
    #fetch second page
    items = unwrap(paginator.fetchPageItems())
    #fetch first page
    items = unwrap(paginator.fetchPageItems())
    #persist
    paginator.reset()

    #restart opertion
    state = State()
    mocker = api_mock([fourth_page, third_page, second_page,first_page])
    paginator = Paginator(options, mocker, state)

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == fourth_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == third_page

    paginator.next()
    items = unwrap(paginator.fetchPageItems())
    assert items == None    