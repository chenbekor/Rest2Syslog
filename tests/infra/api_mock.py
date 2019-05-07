from tests.infra.data import empty_page

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

class MockAPIAdaptor:
    def __init__(self,pages):
        self.setPages(pages)
    
    def setPages(self,pages):
        self.mock_response = MockResponse(pages = pages)

    def fetchItems(self, page):
        return self.mock_response.json()
    
def api_mock(pages = empty_page):
    return MockAPIAdaptor(pages)