import sys
import requests
import csv
import os
import MySQLdb
import settings
import time
import selenium
from selenium import webdriver

PHANTOMJS_PATH = settings.PHANTOMJS_PATH

browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
print('PhantomJS initializing')
browser.implicitly_wait(3)

def set_wait_time(time):
    browser.set_page_load_timeout(time)

def login(user, pass_word):
    #ログインページにアクセス
    url_login = 'https://rikunabi-direct.jp/2020/login/'
    browser.get(url_login)
    #アクセス判定。アクセスできなかったら終了する
    test = requests.get(url_login)
    status_code = test.status_code
    if status_code == 200:
        print('HTTP status code ' + str(status_code) + ':ログインページにアクセス')
    else:
        print('HTTP status code ' + str(test.status_code) + ':ログインページにアクセスできませんでした')
        sys.exit()
    time.sleep(5)
    #userとパスワードを入力
    #user
    element = browser.find_element_by_name('accountId')
    element.clear()
    element.send_keys(user)
    print('userを入力しました')
    #パスワード
    element = browser.find_element_by_name('password')
    element.clear()
    element.send_keys(pass_word)
    print('パスワードを入力しました')
    #送信
    submit = browser.find_element_by_xpath("//img[@alt='ログイン']")
    submit.click()
    print('ログインボタンを押しました')

def check_current_url():
    current_page_url = browser.current_url
    print('現在のURL: ' + current_page_url)

def move_to_company_list():
    #全掲載企業のページに移動する
    element = browser.find_element_by_link_text('全掲載企業')
    element.click()
    #別のタブで開かれるので、二つ目のタブに移動する
    browser.switch_to_window(browser.window_handles[1])
    print('新たにタブを開き、移動しました')

#全掲載企業のURLを取得
def get_url(number_of_company):
    url_arr = []
    for i in range(2, number_of_company):
        url_xpath = '/html/body/div/div/table/tbody/tr[{0}]/td/ul/li/a'.format(i)

        element = browser.find_element_by_xpath(url_xpath)
        url = element.get_attribute('href')
        url_arr.append(url)

        print(str(i))
        print(url)

    return url_arr

#配列をCSVに書き出し
def export_csv(arr, csv_path):
    with open(csv_path, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(arr)

#現在のタブを閉じてトップページに戻る
def browser_close():
    browser.close()
    browser.switch_to_window(browser.window_handles[0])
    #check_current_url()

def import_csv(csv_path):
    if os.path.exists(csv_path) == True:
        with open(csv_path, 'r') as f:
            data = list(csv.reader(f))#二次元配列. 0番目の要素がURLの配列になっている.
        return data[0]
    else:
        print('csvが存在しません')
        sys.exit()

def open_new_page(url):
    browser.execute_script('window.open()')
    browser.switch_to_window(browser.window_handles[1])
    browser.get(url)

def is_exist_casual():
    casual_flag = False
    try:
        for i in range(1, 3+1):
            feature_element = browser.find_element_by_xpath('//*[@id="contents"]/div[9]/div/dl[{0}]/dt'.format(i))
            if feature_element.text == 'カジュアルな服装':
                casual_flag == True
    except selenium.common.exceptions.NoSuchElementException:
        print('特徴が3つ未満です')
    return casual_flag
    

def content_scraping(corsor, connector):
    #時間系計測を行う
    get_text_time_start = time.time()
    name_element = browser.find_element_by_class_name('companyDetail-companyName')
    position_element = browser.find_element_by_xpath('//div[@class="companyDetail-sectionBody"]/p[1]')
    job_description_element = browser.find_element_by_xpath('//div[@class="companyDetail-sectionBody"]/p[2]')
    company_name = name_element.text
    position = position_element.text
    job_description = job_description_element.text
    url = browser.current_url
    get_text_time = time.time() - get_text_time_start

    get_casual_flag_time_start = time.time()
    casual_flag = is_exist_casual()
    get_casual_flag_time = time.time() - get_casual_flag_time_start

    db_insert_time_start = time.time()
    #----------以下DB登録処理----------#  
    #INSERT
    corsor.execute('INSERT INTO company_data SET name="{0}", url="{1}", position="{2}", description="{3}", is_casual="{4}"'.format(company_name, url, position, job_description, casual_flag))
    connector.commit()
    db_insert_time = time.time() - db_insert_time_start

    print('get_text_time:{0}(s)'.format(get_text_time))
    print('get_casual_time:{0}(s)'.format(get_casual_flag_time))
    print('db_insert_time:{0}(s)'.format(db_insert_time))

    
