import re


class IdentifierProcessorMetaclass(type):
    """
    Metaclass that is aggregating *identifier* attributes from all
    parent classes and transform it into regular expressions patterns
    """
    def __new__(cls, clsname, bases, dct):
        for base in bases:
            try:
                for element in base.identifier:
                    dct["identifier"].append(element)
            except (KeyError, AttributeError):  # Pass when baseclass or subclass has not attrib "identifier"
                pass

        try:
            dct["identifier"] = map(lambda x: re.compile(x), dct["identifier"])
        except KeyError:
            pass

        return super(IdentifierProcessorMetaclass, cls).__new__(cls, clsname, bases, dct)


class PowerPage(object):
    """
    Base class for Page Objects
    """
    __metaclass__ = IdentifierProcessorMetaclass

    def __init__(self, driver, scenario):
        self.driver = driver
        self.scenario = scenario

    def execute(self):
        raise NotImplemented("Actions have to overwrite this method!")