from selenium.webdriver.firefox.webdriver import WebDriver


class WikiHomePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def english(self):
        return self.driver.find_element_by_id('js-link-box-en')

    def spanish(self):
        return self.driver.find_element_by_id('js-link-box-es')

    def search_button(self):
        return self.driver.find_element_by_xpath(('//'))