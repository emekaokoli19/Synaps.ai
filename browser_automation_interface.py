from abc import ABC, abstractmethod


class BrowserAutomationInterface(ABC):
    @abstractmethod
    def get_page_source(self):
        raise NotImplementedError

    @abstractmethod
    def find_element(self, by, value):
        raise NotImplementedError

    @abstractmethod
    def navigate_to(self, url):
        raise NotImplementedError

    @abstractmethod
    def go_back(self):
        raise NotImplementedError


class SeleniumAdapter(BrowserAutomationInterface):
    def __init__(self, driver):
        self.driver = driver

    def get_page_source(self):
        return self.driver.page_source

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def navigate_to(self, url):
        self.driver.get(url)

    def go_back(self):
        self.driver.back()

    def quit(self):
        self.driver.quit()