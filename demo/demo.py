from twested import Reactor
from twested.adapters import Selenium

from pages import Homepage, SingleSearchResult, NoSearchResult, MultipleSearchResults


class PerformSearch(Homepage):
    def execute(self):
        self.search(self.context["search_phrase"])


class SingleResultFound(SingleSearchResult):
    def execute(self):
        print "Single repository found!"


class MultipleResultsFound(MultipleSearchResults):
    def execute(self):
        print "Multiple repositories found!"


class NoResultFound(NoSearchResult):
    def execute(self):
        print "No repositories found!"

if __name__ == "__main__":
    context = {"search_phrase": "tested\n"}

    driver = Selenium()
    reactor = Reactor(driver)
    reactor.add_callback(PerformSearch)
    reactor.add_callbacks(SingleResultFound, (MultipleResultsFound, NoResultFound))
    reactor.run(entry_url='https://github.com/', context=context)
