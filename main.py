from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time

def doMacro():
    driver = webdriver.Chrome()
    url = 'https://cyber.inu.ac.kr/login.php'
    driver.get(url)
    action = ActionChains(driver)  # action을 이용하여 driver 조정

    # out_button = driver.find_element_by_css_selector()

    # input id, pw
    site_id = input()
    site_pw = input()
    driver.find_element_by_css_selector('#input-username').send_keys(site_id)
    driver.find_element_by_css_selector('#input-password').send_keys(site_pw)
    action.send_keys(Keys.ENTER).perform().reset_actions()

    time.sleep(0.5)
    # driver.find_elements_by_css_selector('.left-menu-link.left-menu-link-mypage')[2].click()

from tkinter import *

win = Tk()
win.title("Video Play Macro")
win.geometry("300x500")
win.option_add("*Font", "맑은고딕 14")

# C_Var1 = IntVar()
# C_Var2 = IntVar()
# Check1 = Checkbutton(win, text = '인천대', variable = C_Var1, onvalue = 1, offvalue = 0)
# Check2 = Checkbutton(win, text = '인하대', variable = C_Var2, onvalue = 1, offvalue = 0)
#
# Check1.pack()
# Check2.pack()

radioValue = IntVar()
radio1 = Radiobutton(win, text="인천대", variable=radioValue, value=1)
radio2 = Radiobutton(win, text="인하대", variable=radioValue, value=2)

radio1.pack()
radio2.pack()
# radio1.grid(column=0, row=0)
# radio2.grid(column=0, row=1)

url = 'https://cyber.inu.ac.kr/login.php'
def radioFunc():
    if radioValue.get() == 1:
        url = 'https://cyber.inu.ac.kr/login.php'
    elif radioValue.get() == 2:
        url = 'https://learn.inha.ac.kr/login.php'
    print(url)



btn = Button(win, text="출력", command = radioFunc())
btn.pack()

# def btnFunc():
#     if C_Var1.get() == 1 and C_Var2.get() == 0:
#         url = 'https://cyber.inu.ac.kr/login.php'
#     elif C_Var1.get() == 0 and C_Var2.get() == 1:
#         url = 'https://learn.inha.ac.kr/login.php'
#
#     print(url)
#
# btn = Button(win, text = "출력", command = btnFunc)
# btn.pack()

win.mainloop()

