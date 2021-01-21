from selenium import webdriver

driver = webdriver.Chrome()
url = 'https://cyber.inu.ac.kr'
driver.get(url)


# 아이디 비밀번호 입력
driver.find_element_by_css_selector('.required.form-control').send_keys('201901739')
driver.find_element_by_css_selector('.required.form-control').send_keys('201901739')