from selenium import webdriver

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from time import sleep

from random import randint

Social_IDs = ['E125491173', 'E126112386', "E126054870", 'T126128215', 'E126257415', 'E126367612', 'A131228879', 'A130626871', 'E126249575', 'S125819172', 'E126112199','E126110846', "Q124534070"]

for i in Social_IDs:
	driver = webdriver.Chrome()

	try:

		driver.get("https://webap1.kshs.kh.edu.tw/kshsSSO/publicWebAP/bodyTemp/index.aspx")

		driver.find_element_by_id("ContentPlaceHolder1_txtId").send_keys(i)
 
		driver.find_element_by_id("ContentPlaceHolder1_btnId").click()

		driver.find_element_by_id("ContentPlaceHolder1_rbType_1").click()

		s1 = Select(driver.find_element_by_id('ContentPlaceHolder1_ddl1'))
		s2 = Select(driver.find_element_by_id('ContentPlaceHolder1_ddl2'))

		s3 = Select(driver.find_element_by_id('ContentPlaceHolder1_ddl3'))

		s1.select_by_index(2)

		s2.select_by_index(randint(3, 8))

		s3.select_by_index(1)
		
		driver.find_element_by_id("ContentPlaceHolder1_btnId0").click()
		driver.close()
	except :
		driver.close()
	print(i)

		