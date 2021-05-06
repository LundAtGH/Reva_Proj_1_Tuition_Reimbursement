from behave import when, then
from selenium.webdriver.firefox.webdriver import WebDriver


@when(u'The User types {word} in the search bar')
def type_into_searchbar(context, word):
    context.wiki_home_page.search_bar().send_keys(word)


@when(u'The User clicks the search button')
def press_search_button(context):
    context.wiki_home_page.search_button().click()


@then(u'The title should be {title} - Wikipedia')
def step_impl(context, title):
    driver: WebDriver = context.driver
    assert driver.title == title