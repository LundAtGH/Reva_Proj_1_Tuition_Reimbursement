from behave import given, when, then
from selenium.webdriver.firefox.webdriver import WebDriver

from features.pages.wiki_home import WikiHomePage


@given('The User is on the Wikipedia Home Page')
def get_to_wiki_home(context):
    driver: WebDriver = context.driver
    driver.get('https://www.wikipedia.org/')


@when('The User clicks on English')
def nav_to_english(context):
    context.wiki_home_page.english().click()


@then('The User should be on the English Home Page')
def verify_on_english(context):
    driver: WebDriver = context.driver
    assert driver.title == "Wikipedia, the free encyclopedia"


@when('The User clicks on Spanish')
def nav_to_spanish(context):
    context.wiki_home_page.spanish().click()


@then('The User should be on the Spanish Home Page')
def verify_on_spanish(context):
    driver: WebDriver = context.driver
    assert driver.title == "Wikipedia, la enciclopedia libre"
