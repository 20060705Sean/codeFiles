from selenium import webdriver

from xrange import xrange

driver = webdriver.Chrome()

driver.get("https://popcat.click/")

a = driver.find_element_by_css_selector("[src='/img/popcat.4158e1f3.svg']")

for i in xrange(10000):
	a.click();a.click();a.click();a.click();a.click();a.click();a.click();a.click();a.click();a.click()

driver.close()