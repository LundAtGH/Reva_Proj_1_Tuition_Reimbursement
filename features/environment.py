from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver


# All setup and teardown functions must go in this file.
# These functions must be named using behave's conventions.
from features.pages.wiki_home import WikiHomePage


def before_all(context):
    # Project 1 not required to be run with
    # these options set for driver:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    path = r'C:\Users\klund\Desktop\Rev_3_Mo_Program\geckodriver'
    driver: WebDriver = webdriver.Firefox(
        executable_path=path,
        firefox_options=options
    )

    wiki_home_page = WikiHomePage(driver)

    context.driver: WebDriver = driver
    context.wiki_home_page = wiki_home_page
    print("Started.")


def after_all(context):
    context.driver.quit()
    print("Ended.")
