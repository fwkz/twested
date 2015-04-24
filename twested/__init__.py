import re
from collections import deque, Iterable


class Reactor(object):
    def __init__(self, driver_adapter):
        self.driver_adapter = driver_adapter
        self.driver = None

        self.callback_chain = deque()
        self.errback_chain = deque()

    def add_callback(self, callback):
        self.callback_chain.append(callback)
        self.errback_chain.append(CallbackMock)

    def add_callbacks(self, callback, errback):
        self.callback_chain.append(callback)
        self.errback_chain.append(errback)

    def add_errback(self, errback):
        self.callback_chain.append(CallbackMock)
        self.errback_chain.append(errback)

    def add_both(self, callback):
        self.callback_chain.append(callback)
        self.errback_chain.append(callback)

    def run(self, entry_url, context=None):
        """ Main Reactor body.

        Check which Page Object is loaded into webdriver and execute handler that it tied with it.
        """
        self.driver = self.driver_adapter()
        self.driver.navigate(entry_url)

        while self.callback_chain:
            callback = self.callback_chain.popleft()
            errback = self.errback_chain.popleft()
            errback = errback if isinstance(errback, Iterable) else (errback, )  # Errback is always in form of tuple
            currently_loaded_page_url = self.driver.current_url.lower()
            currently_loaded_page_body = self.driver.response_body

            match = lambda callback: callback.path.lower() in currently_loaded_page_url and\
                                     all(re.search(element, currently_loaded_page_body) for element in callback.identifier)

            if match(callback):
                try:
                    callback(self.driver, context).execute()
                except:
                    self.stop()
                    raise
            elif any([match(err) for err in errback]):
                actual_errback = errback[[match(err) for err in errback].index(True)]
                try:
                    actual_errback(self.driver, context).execute()
                except:
                    raise
                else:
                    raise Exception("Errback {} was triggered!".format(actual_errback))
                finally:
                    self.stop()
            else:
                self.stop()
                raise Exception("There is no proper handler for page {}\n\n"
                                "Current callback: {}".format(currently_loaded_page_url, callback))
        self.stop()

    def stop(self):
        self.driver.quit()
        self.callback_chain.clear()
        self.errback_chain.clear()


class NonEqualAttribute(object):
    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True


class CallbackMock(object):
    path = NonEqualAttribute()
    identifier = NonEqualAttribute()

    def execute(self):
        pass
