from twested.power_page import PowerPage


class Homepage(PowerPage):
    path = "/"
    identifier = ['Build software better, together.']

    def search(self, phrase):
        element = self.driver.find_element_by_css_selector(".js-site-search-focus")
        element.send_keys(phrase)


class SearchResults(PowerPage):
    path = '/search'
    identifier = ['Repositories']


class SingleSearchResult(SearchResults):
    identifier = ['<span class="counter">1</span>']


class MultipleSearchResults(SearchResults):
    identifier = ['<span class="counter">(\d+,?)+</span>']


class NoSearchResult(SearchResults):
    identifier = ["We couldn't find any repositories matching"]