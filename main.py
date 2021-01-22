from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk, StringVar


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
url = []
playlist = []

def loginFunc():
    if cb_sch.get() == "인천대학교":
        url = 'https://cyber.inu.ac.kr/login.php'
    elif cb_sch.get() == "인하대학교":
        url = 'https://learn.inha.ac.kr/login.php'
    driver.get(url)
    str_id = tb_id.get()
    str_pw = tb_pw.get()
    driver.find_element_by_css_selector('#input-username').send_keys("12180481")  # str_id
    driver.find_element_by_css_selector('#input-password').send_keys("01230123bb1!")  # str_pw
    driver.find_element_by_css_selector('#input-password').send_keys(Keys.ENTER)

    driver.find_element_by_css_selector('span.close_notice').click() #안내 창 닫아

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    crs_name = soup.select('.course-name')

    crs_list = []
    for i in crs_name:
        crs_list.append(i.select_one('.course-title').text) #리스트에 과목명 저장
   # print(crs_list)

    def combo_save1(event):
        playlist.append(crs_combo1.get())
        print(playlist)

    def combo_save2(event):
        playlist.append(crs_combo2.get())
        print(playlist)

    def combo_save3(event):
        playlist.append(crs_combo3.get())
        print(playlist)

    crs_combo1 = ttk.Combobox(win, value=crs_list)
    crs_combo1.grid(row=5, column=1)
    crs_combo1.bind("<<ComboboxSelected>>", combo_save1)


    crs_combo2 = ttk.Combobox(win, value=crs_list)
    crs_combo2.grid(row=6, column=1)
    crs_combo2.bind("<<ComboboxSelected>>", combo_save2)

    crs_combo3 = ttk.Combobox(win, value=crs_list)
    crs_combo3.grid(row=7, column=1)
    crs_combo3.bind("<<ComboboxSelected>>", combo_save3)




    btn_macro = Button(win, text="Macro", command=macroFunc)
    btn_macro.grid(row=8, column=1)

btn_login = Button(win, text="LOG IN", command=loginFunc)
btn_login.grid(row=4, column=1)



def macroFunc():
    url = driver.current_url
    #print(url)
    # html = urllib.request.urlopen(url).read()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find_all(class_='course_link')

    crs_link = []
    for i in title:
        crs_link.append(i.attrs['href'])
    print(crs_link)



win.mainloop() # 창 실행



# div class = "progress_courses"