from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk, StringVar
import re  # 숫자 추출용
import time  # 현재 시간 추출용
from datetime import datetime

import time

# gui 창 생성
win = Tk()
win.geometry("300x330") #크기
win.title("MAGIC MACRO")
win.option_add("*Font", "맑은고딕 12")

# 학교 선택
lb_school = Label(win, text='학교명')
lb_school.grid(row=0, column=0)

cb_sch = ttk.Combobox(win, values=["인천대학교"])
print(dict(cb_sch))
cb_sch.grid(row=0, column=1)
cb_sch.current(0)
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
crs_list = ['x']
is_login = False
def loginFunc(*args):
    if cb_sch.get() == "인천대학교":
        url = 'https://cyber.inu.ac.kr/login.php'


    driver.get(url)
    str_id = tb_id.get()
    str_pw = tb_pw.get()
    driver.find_element_by_css_selector('#input-username').send_keys(str_id)  # str_id
    driver.find_element_by_css_selector('#input-password').send_keys(str_pw)  # str_pw
    driver.find_element_by_css_selector('#input-password').send_keys(Keys.ENTER)


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    crs_name = soup.select('.course-name')

    for i in crs_name:
        crs_list.append(i.select_one('.course-title').text) #리스트에 과목명 저장
    print(crs_list)

    if driver.current_url != url:
        is_login = True

    global crs_combo1, crs_combo2

    crs_combo1 = ttk.Combobox(win, value=crs_list)
    crs_combo1.current(0)
    crs_combo1.grid(row=5, column=1)

    crs_combo2 = ttk.Combobox(win, value=crs_list)
    crs_combo2.current(0)
    crs_combo2.grid(row=6, column=1)

    btn_macro = Button(win, text="Macro", command=macroFunc)
    btn_macro.grid(row=14, column=1)


btn_login = Button(win, text="LOG IN", command=loginFunc)
btn_login.grid(row=4, column=1)

def getIdx(combo):
    i = 0
    while combo.current(i) != crs_list[i]:
        i = i + 1
    return i



def macroFunc():
    url = driver.current_url
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find_all(class_='course_link')
    crs_link = []
    print(title)
    for i in title:
        print(i.attrs['href'])
        crs_link.append(i.attrs['href'])

    crs_idx = 0

# combobox 첫번째
    for i in range(len(crs_list)):
        if crs_combo1.get() == crs_list[i]:
            crs_idx = i
            break

    if crs_idx == 0:    # 아무것도 선택 안된 경우 (종료 또는 오류메세지 출력)
        print("========종료============")
    else:
        # 선택된 강의 url 불러오기
        url = crs_link[crs_idx-1]
        driver.get(url)

        # 크롤링 요소
        html_crs = driver.page_source
        soup_crs = BeautifulSoup(html_crs, 'html.parser')
        crs_class = soup_crs.find_all(class_='activity vod modtype_vod')
        print('crs_class')
        print(crs_class)

        # 출석 인정 날짜 추출
        crs_date = []
        for i in crs_class:
            s_date = "".join(re.findall("\d+", i.select_one('.text-ubstrap').text)[:6])
            f_date = "".join(re.findall("\d+", i.select_one('.text-ubstrap').text)[6:])
            crs_date.append(s_date)
            crs_date.append(f_date)

        # 현재 시간 가져오기
       # n_date = datetime.today().strftime("%Y%m%d%H%M%S")
        n_date ='20210702101010'

        # 비디오 링크 크롤링
        soup_crs_video = BeautifulSoup(html_crs, 'html.parser')
        crs_video_class = soup_crs_video.find_all('a')

        # 비디오 링크 추출
        temp = []
        for i in crs_video_class:
            temp.append(i.get('href'))

        video_link = []
        for i in range(len(temp)):
            if re.findall("vod", str(temp[i])) != []:
                video_link.append(temp[i])
        video_link = video_link[1:]  # 제일 처음에 동영상이 아닌 링크가 섞여 있음 (해결해야함)
        print(video_link)

        # 출석 인정 시간과 비교하여 실행행
        for i in range(len(crs_date)//2):
            s_date_idx = 2*i
            f_date_idx = 2*i + 1
            if int(crs_date[s_date_idx]) <= int(n_date) and int(n_date) <= int(crs_date[f_date_idx]):  # ==> 지금 출석처리 기간인 영상이 없음 ==> 나중에 not 빼줘야함
                # 이미 출석 처리 된 강의 제외하는 부분 추가해야함
                url = video_link[i]
                driver.execute_script('window.open("");')

                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)

                html_video = driver.page_source
                soup_video = BeautifulSoup(html_video, 'html.parser')
                class_video = soup_video.select('div.buttons')[0]
                #print(class_video)
                url = class_video.select('a')[0].get('href')


                driver.get(url)
                driver.find_element_by_id('vod_player').click()  # 재생 클릭


                html_video_time = driver.page_source
                #print('html_video_time',html_video_time)
                time.sleep(3)
                soup_video_time = BeautifulSoup(html_video_time, 'html.parser')
                remaining_time = re.findall("\d+",
                                            soup_video_time.find(class_='jw-text jw-reset jw-text-duration').text)

                print('sssss',soup_video_time.find(class_='jw-text jw-reset jw-text-duration'))


                # 남은 시간 초로 변환
                while len(remaining_time) != 1:
                    i = 0
                    remaining_time[i+1] = int(remaining_time[i+1]) + int(remaining_time[i])*60
                    del remaining_time[i]
                remaining_sec = remaining_time[0]  # int형으로 변환

                # 위에서 받아온 시간만큼 기다리기
               # time.sleep(remaining_sec + 60)  # time.sleep(1) # 확인하기에 너무 길어서 10초로 설정
                time.sleep(3)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
# combobox 두번째
    for i in range(len(crs_list)):
        if crs_combo2.get() == crs_list[i]:
            crs_idx = i
            break

    if crs_idx == 0:    # 아무것도 선택 안된 경우 (종료 또는 오류메세지 출력)
        print("========종료============")
    else:
        # 선택된 강의 url 불러오기
        url = crs_link[crs_idx-1]
        driver.get(url)

        # 크롤링 요소
        html_crs = driver.page_source
        soup_crs = BeautifulSoup(html_crs, 'html.parser')
        crs_class = soup_crs.find_all(class_='activity vod modtype_vod')
        print('crs_class')
        print(crs_class)

        # 출석 인정 날짜 추출
        crs_date = []
        for i in crs_class:
            s_date = "".join(re.findall("\d+", i.select_one('.text-ubstrap').text)[:6])
            f_date = "".join(re.findall("\d+", i.select_one('.text-ubstrap').text)[6:])
            crs_date.append(s_date)
            crs_date.append(f_date)

        # 현재 시간 가져오기
       # n_date = datetime.today().strftime("%Y%m%d%H%M%S")
        n_date ='20210702101010'

        # 비디오 링크 크롤링
        soup_crs_video = BeautifulSoup(html_crs, 'html.parser')
        crs_video_class = soup_crs_video.find_all('a')

        # 비디오 링크 추출
        temp = []
        for i in crs_video_class:
            temp.append(i.get('href'))

        video_link = []
        for i in range(len(temp)):
            if re.findall("vod", str(temp[i])) != []:
                video_link.append(temp[i])
        video_link = video_link[1:]  # 제일 처음에 동영상이 아닌 링크가 섞여 있음 (해결해야함)
        print(video_link)

        # 출석 인정 시간과 비교하여 실행행
        for i in range(len(crs_date)//2):
            s_date_idx = 2*i
            f_date_idx = 2*i + 1
            if int(crs_date[s_date_idx]) <= int(n_date) and int(n_date) <= int(crs_date[f_date_idx]):  # ==> 지금 출석처리 기간인 영상이 없음 ==> 나중에 not 빼줘야함
                # 이미 출석 처리 된 강의 제외하는 부분 추가해야함
                url = video_link[i]
                driver.execute_script('window.open("");')

                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)

                html_video = driver.page_source
                soup_video = BeautifulSoup(html_video, 'html.parser')
                class_video = soup_video.select('div.buttons')[0]
                #print(class_video)
                url = class_video.select('a')[0].get('href')


                driver.get(url)
                driver.find_element_by_id('vod_player').click()  # 재생 클릭


                html_video_time = driver.page_source
                #print('html_video_time',html_video_time)
                time.sleep(3)
                soup_video_time = BeautifulSoup(html_video_time, 'html.parser')
                remaining_time = re.findall("\d+",
                                            soup_video_time.find(class_='jw-text jw-reset jw-text-duration').text)

                print('sssss',soup_video_time.find(class_='jw-text jw-reset jw-text-duration'))


                # 남은 시간 초로 변환
                while len(remaining_time) != 1:
                    i = 0
                    remaining_time[i+1] = int(remaining_time[i+1]) + int(remaining_time[i])*60
                    del remaining_time[i]
                remaining_sec = remaining_time[0]  # int형으로 변환

                # 위에서 받아온 시간만큼 기다리기
               # time.sleep(remaining_sec + 60)  # time.sleep(1) # 확인하기에 너무 길어서 10초로 설정
                time.sleep(3)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])


win.mainloop() # 창 실행
