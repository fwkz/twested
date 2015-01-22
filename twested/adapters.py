class BaseDriverAdapter(object):
    def navigate(self, url):
        raise NotImplemented()

    @property
    def response_body(self):
        raise NotImplemented()

    @property
    def current_url(self):
        raise NotImplemented()

    def quit(self):
        raise NotImplemented()

    def execute_script(self, script):
        raise NotImplemented()


class Selenium(BaseDriverAdapter):
    def __init__(self):
        from selenium import webdriver
        self.driver = webdriver.Firefox()

    def __getattr__(self, item):
        return getattr(self.driver, item)

    def navigate(self, url):
        self.driver.get(url)

    @property
    def response_body(self):
        return self.driver.page_source

    @property
    def current_url(self):
        return self.driver.current_url

    def quit(self):
        self.driver.quit()

    def execute_script(self, script):
        self.driver.execute_script(script)