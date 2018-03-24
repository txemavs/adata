from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('http://www.yahoo.com')
assert 'Yahoo' in browser.title

elem = browser.find_element_by_name('uh-search-box')  # Find the search box
elem.send_keys('selenium')
elem.send_keys(u'\ue007')
browser.quit()