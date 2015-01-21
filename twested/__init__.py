from collections import deque


class Reactor(object):
    def __init__(self, driver_adapter=None):
        self.driver = driver_adapter()
        self.entry_url = None

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

    def run(self, entry_url, scenario=None):
        """ Main Reactor body.

        Check which Page Object is loaded into webdriver and execute handler that it tied with it.
        """

        self.driver.navigate(entry_url)

        while self.callback_chain:
            callback = self.callback_chain.popleft()
            errback = self.errback_chain.popleft()
            currently_loaded_page_url = self.driver.current_url.lower()

            if callback.path.lower() in currently_loaded_page_url:
                try:
                    callback(self.driver.driver, scenario).execute()
                except:
                    self.stop()
                    raise
            elif errback.path.lower() in currently_loaded_page_url:
                try:
                    errback(self.driver.driver, scenario).execute()
                except:
                    self.stop()
                    raise
            else:
                self.stop()
                raise Exception("There is no proper handler for page {}\n\n"
                                "Current callback: {}".format(currently_loaded_page_url, callback))
        self.stop()

    def stop(self):
        self.driver.quit()
        self.callback_chain.clear()
        self.errback_chain.clear()


class CallbackMock(object):
    path = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'  # String that is not suppose to match anything

    def execute(self):
        pass