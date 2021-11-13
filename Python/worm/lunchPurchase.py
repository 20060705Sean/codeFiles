from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep																																												
from time import localtime

driver = webdriver.Chrome()
bentonOrder = ["大家鐵路1", "大家鐵路2", "大家鐵路3", "太師傅1", "太師傅2", "太師傅3", "正園A", "正園B", "正園羊肉", "吉樂米1", "吉樂米2", "吉樂米3", "吉樂米－素食", "米寶1", "米寶3", "米寶－方便素", "彩鶴"]
price = [65, 70, 75, 70, 65, 60, 55, 55, 55, 60, 70, 80, 60, 60, 75, 60, 50]
''
driver.get("https://docs.google.com/spreadsheets/d/1dump8rjkC4kWmRz5xnBwbL7AQW4tVlHteLKJGakcdCE/edit?usp=sharing")

def get_grid(grid):
	driver.find_element_by_id("t-name-box").clear()
	driver.find_element_by_id("t-name-box").send_keys(grid+Keys.RETURN)
	return driver.find_elements_by_xpath("//div[@id='t-formula-bar-input']/div[1]")[0].get_attribute('innerHTML').strip()[:-4]
def get_someone_eat_what(i):
	seat = get_grid(f"C{i}")
	benton = ""
	if seat != "":
		benton = get_grid(f"B{i}").split()
	return (seat, benton)
def get_all_order():
	benton = {}
	i = 2
	while True:
		now = get_someone_eat_what(i)
		if now[0] == "":
			i += 1
			continue
		break
	while True:
		now = get_someone_eat_what(i)
		if now[0] == "":
			return benton
		if now[1][0] in list(benton.keys()):
			benton[now[1][0]].append(now[0])
		else:
			benton[now[1][0]] = [now[0]]
		i += 1
bentons = get_all_order()
print(bentons)
bentonsAmount = {i: len(q) for i, q in zip(list(bentons.keys()), list(bentons.values()))}
print(bentonsAmount)
driver.get("https://webap1.kshs.kh.edu.tw/kshsSSO/")
driver.find_element_by_id("ContentPlaceHolder1_txtID").send_keys("104028")
driver.find_element_by_id("ContentPlaceHolder1_txtPassword").send_keys("sean9575")
sleep(5)
driver.find_element_by_id("ContentPlaceHolder1_lbLogin").click()
sleep(15)
total = 0
for i in bentonsAmount:
	select = Select(driver.find_element_by_id(f"ContentPlaceHolder1_gvLunch_ddlAmount_{bentonOrder.index(i)}"))
	select.select_by_index(bentonsAmount[i])
	total += (price[bentonOrder.index(i)] * bentonsAmount[i])
print(total)
with open("lunchOwedMoney.txt", "a", encoding="utf-8") as file:
	file.write("-" * 30 + "\n")
	file.write(f"Date:{localtime().tm_mon}/{localtime().tm_mday}" + "\n")
	for i in bentons:
		for j in bentons[i]:
			file.write(f"X | {j} : {price[bentonOrder.index(i)]} --- {i}" + "\n")
	file.write(f"total : {total}" + "\n")
driver.find_element_by_id("ContentPlaceHolder1_btnUpdate").click()
driver.close()