from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://popass.click/")

a = driver.find_element_by_css_selector("[src='/img/logo.d7751fae.png']")

for i in range(244):
	a.click()

driver.close()