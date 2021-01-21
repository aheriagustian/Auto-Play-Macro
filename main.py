
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk, StringVar
from tkinter import messagebox

import time

# gui 창 생성
win = Tk()
win.geometry("300x300") #크기
win.title("MAGIC MACRO")
win.option_add("*Font", "맑은고딕 12")

# 학교 선택
lb_school = Label(win, text='학교명')
lb_school.grid(row=0, column=0)

cb_sch = ttk.Combobox(win, values=["서울대학교", "연세대학교", "인천대학교", "인하대학교"])
print(dict(cb_sch))
cb_sch.grid(row=0, column=1)
cb_sch.current(3)
print(cb_sch.current(), cb_sch.get())

# 로그인
lb_id = Label(win, text=' ID ')
lb_id.grid(row=2, column=0)

str_id = StringVar()
tb_id = ttk.Entry(win, width=20)
tb_id.grid(row=2, column=1)

lb_pw = Label(win, text=' PW ')
lb_pw.grid(row=3, column=0)

str_pw: StringVar = StringVar()
tb_pw = ttk.Entry(win, width=20)
tb_pw.grid(row=3, column=1)

driver = webdriver.Chrome()
def loginFunc():
    if cb_sch.get() == "인천대학교":
        url = 'https://cyber.inu.ac.kr/login.php'
    elif cb_sch.get() == "인하대학교":
        url = 'https://learn.inha.ac.kr/login.php'
    driver.get(url)
    str_id = tb_id.get()
    str_pw = tb_pw.get()
    driver.find_element_by_css_selector('#input-username').send_keys(str_id)  # str_id
    driver.find_element_by_css_selector('#input-password').send_keys(str_pw)  # str_pw
    driver.find_element_by_css_selector('#input-password').send_keys(Keys.ENTER)

btn_login = Button(win, text="LOG IN", command=loginFunc)
btn_login.grid(row=4, column=1)


# 강의검색
lb_lec = Label(win, text=' [ PLAY LIST ]')
lb_lec.grid(row=5, column=0)

lb_lec1 = Label(win, text=' 1st ')
lb_lec1.grid(row=6, column=0)

str_lec1 = StringVar()
tb_lec1 = ttk.Entry(win, width=20, textvariable=str_lec1)
tb_lec1.grid( row = 6, column = 1)

lb_lec2 = Label(win, text=' 2nd ')
lb_lec2.grid(row=7, column=0)

str_lec2 = StringVar()
tb_lec2 = ttk.Entry(win, width=20, textvariable=str_lec2)
tb_lec2.grid( row = 7, column = 1)

lb_lec3 = Label(win, text=' 3rd ')
lb_lec3.grid(row=8, column=0)

str_lec3 = StringVar()
tb_lec3 = ttk.Entry(win, width=20, textvariable=str_lec3)
tb_lec3.grid( row = 8, column = 1)

btn_play = Button(win, text="PLAY")
btn_play.grid(row=9, column=1)





win.mainloop() # 창 실행



# div class = "progress_courses"