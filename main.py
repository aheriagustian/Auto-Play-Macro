from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
url = 'https://cyber.inu.ac.kr'
driver.get(url)


# 아이디 비밀번호 자동입력
driver.find_element_by_css_selector('#input-username').send_keys('201901739')
driver.find_element_by_css_selector('#input-password').send_keys('sh9230915!')
# 비번창에서 그냥 엔터
driver.find_element_by_css_selector('#input-password').send_keys(Keys.ENTER)

