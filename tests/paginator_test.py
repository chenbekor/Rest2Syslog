from r2s_paginator import Paginator
from r2s_state import State

options = {'max_pages':1}
empty_page = []
first_page = [{'id':'1'},{'id':'2'},{'id':'3'}]
second_page = [{'id':'4'},{'id':'5'},{'id':'6'}]
two_pages = [first_page,second_page]
class MockResponse:
    def __init__(self,status_code = 200, pages = empty_page):
        self.status_code = status_code
        self.current_page = 0
        self.pages = pages
        self.total_pages = len(pages)

    def json(self):
        if self.current_page < self.total_pages:
            page = self.pages[self.current_page]
            self.current_page +=1
        else:
            page = empty_page

        return {'alerts':page}

class MockAPIHandler:
    def __init__(self,pages):
        self.mock_response = MockResponse(pages = pages)
        
    def executeRequest(self, page):
        return self.mock_response
    
def api(pages = empty_page):
    return MockAPIHandler(pages)

def test_empty_page():
    paginator = Paginator(options, api())
    assert paginator.fetchPage() == None

def test_single_page():
    paginator = Paginator(options, api([first_page]))
    assert paginator.fetchPage() == first_page

def test_no_new_records():
    paginator = Paginator(options, api([first_page]), State(last_record_id='1'))
    assert paginator.fetchPage() == None

def test_1_item():
    paginator = Paginator(options, api([first_page]), State(last_record_id='2'))
    assert paginator.fetchPage() == [{'id':'1'}]

    paginator.next()
    items = paginator.fetchPage()
    assert items == None


def test_two_pages():
    paginator = Paginator(options, api(two_pages))
    
    items = paginator.fetchPage()
    assert items == first_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == second_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == None    

def test_4_items():
    paginator = Paginator(options, api(two_pages), state = State(last_record_id='5'))
    
    items = paginator.fetchPage()
    assert items == first_page

    paginator.next()
    items = paginator.fetchPage()
    assert items == [{'id':'4'}]

    paginator.next()
    items = paginator.fetchPage()
    assert items == None