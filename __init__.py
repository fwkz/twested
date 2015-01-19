from collections import deque


class Reactor(object):
    def __init__(self, driver_adapter=None):
        self.driver = driver_adapter()
        self.entry_url = None

        self.callback_chain = deque()
        self.errback_chain = deque()

    def add_callback(self, callback):
        self.callback_chain.append(callback)
        self.errback_chain.append(None)

    def add_callbacks(self, callback, errback):
        self.callback_chain.append(callback)
        self.errback_chain.append(errback)

    def add_errback(self, errback):
        self.callback_chain.append(None)
        self.errback_chain.append(errback)

    def add_both(self, callback):
        self.callback_chain.append(callback)
        self.errback_chain.append(callback)

    def run(self, entry_url, scenario=None):
        """ Main Reactor body.

        Check which Page Object is loaded into webdriver and execute handler that it tied with it.
        """

        # Navigate to starting point.
        self.driver.navigate(entry_url)

        # Define current url for the first time.
        current_page = self.driver.current_url

        while current_page != self.callback_chain[-1]:  # Run until get to the exit point.
            callback = self.callback_chain.popleft()  # Handle the current page.
            errback = self.errback_chain.popleft()
            try:
                callback.execute(self.driver, scenario)
            except:
                try:
                    errback.execute(self.driver, scenario)
                except:
                    raise Exception("There is no proper handler for page {}".format(current_page))

            # previous_page = current_page
            current_page = self.driver.current_url  # Get the current location.

        callback = self.callback_chain.popleft()  # Handle the current page.
        errback = self.errback_chain.popleft()
        try:
            callback.execute(self.driver, scenario)
        except:
            try:
                errback.execute(self.driver, scenario)
            except:
                raise LookupError("There is no proper callback for page {}".format(current_page))