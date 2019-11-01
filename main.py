import utils
import os
import MySQLdb
import time
import selenium
import settings
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver

USER_ID = settings.USER_ID
PASS_WORD = settings.PASS_WORD
USER_ID_2 = settings.USER_ID_2
PASS_WORD_2 = settings.PASS_WORD_2
TIME_TO_WAIT = 5
NUMBER_OF_COMPANY = 16412
URL_PATH = settings.URL_PATH
DB_UNIX_SOCKET = settings.DB_UNIX_SOCKET
DB_HOST = settings.DB_HOST
DB_USER = settings.DB_USER
DB_PASS_WORD = settings.DB_PASS_WORD
DB_NAME = settings.DB_NAME
PHANTOMJS_PATH = settings.PHANTOMJS_PATH
NUMBER_OF_BROWSERS = 2

browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
print('PhantomJS initializing')
browser.implicitly_wait(3)

browser_2 = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)
print('PhantomJS initializing')
browser.implicitly_wait(3)

browser_arr = [browser, USER_ID, PASS_WORD]
browser_arr_2 = [browser_2, USER_ID_2, PASS_WORD_2]
browsers = [browser_arr, browser_arr_2]

if __name__ == '__main__':
    for browser_param in browsers:
        utils.login(browser_param[1], browser_param[2], browser_param[0])
        utils.set_wait_time(TIME_TO_WAIT, browser_param[0])
        utils.check_current_url(browser_param[0])

    #csvが存在していなかったら、urlを全て配列に格納し、csvとしてエクスポートする
    if os.path.exists(URL_PATH) == False:
        utils.move_to_company_list(browsers[0][0])
        url_arr = utils.get_url(NUMBER_OF_COMPANY, browsers[0][0])
        utils.export_csv(url_arr, URL_PATH)
        utils.browser_close(browsers[0][0])
    else:
        #csvが存在していたら、csvを読み込んでurl_arrに格納する
        url_arr = utils.import_csv(URL_PATH)

    #DB接続
    connector = MySQLdb.connect(
        unix_socket = DB_UNIX_SOCKET,
        host=DB_HOST, user=DB_USER, passwd=DB_PASS_WORD, db=DB_NAME
    )
    corsor = connector.cursor()

    #ブラウザの数だけURLの配列を分割する
    url_arrs = list(np.array_split(url_arr, NUMBER_OF_BROWSERS))
    print(len(url_arrs[0]))
    print(len(url_arrs[1]))

    #各ブラウザでスクレイピング処理を行う（並列処理)
    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="thread") as executor:
        for i in range(NUMBER_OF_BROWSERS):
            executor.submit(utils.scraping_process, browsers[i][0], url_arrs[i], corsor, connector)
        
    print('DONE!')