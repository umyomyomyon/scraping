import utils
import os
import MySQLdb
import time
import selenium
import settings
from selenium import webdriver

USER_ID = settings.USER_ID
PASS_WORD = settings.PASS_WORD
TIME_TO_WAIT = 5
NUMBER_OF_COMPANY = 16412
URL_PATH = settings.URL_PATH
DB_UNIX_SOCKET = settings.DB_UNIX_SOCKET
DB_HOST = settings.DB_HOST
DB_USER = settings.DB_USER
DB_PASS_WORD = settings.DB_PASS_WORD
DB_NAME = settings.DB_NAME
PHANTOMJS_PATH = settings.PHANTOMJS_PATH
NUMBER_OF_BROWSER = 10

if __name__ == '__main__':
    utils.login(USER_ID, PASS_WORD)
    utils.set_wait_time(TIME_TO_WAIT)
    utils.check_current_url()

    #csvが存在していなかったら、urlを全て配列に格納し、csvとしてエクスポートする
    if os.path.exists(URL_PATH) == False:
        utils.move_to_company_list()
        url_arr = utils.get_url(NUMBER_OF_COMPANY)
        utils.export_csv(url_arr, URL_PATH)
        utils.browser_close()
    else:
        #csvが存在していたら、csvを読み込んでurl_arrに格納する
        url_arr = utils.import_csv(URL_PATH)

    #DB接続
    connector = MySQLdb.connect(
        unix_socket = DB_UNIX_SOCKET,
        host=DB_HOST, user=DB_USER, passwd=DB_PASS_WORD, db=DB_NAME
    )
    corsor = connector.cursor()

    #企業ページを開き、そこかスクレイピングを行う
    length = len(url_arr)
    for i in range(length):
        utils.open_new_page(url_arr[i])
        print(i)
        try:
            utils.content_scraping(corsor, connector)
        except selenium.common.exceptions.NoSuchElementException:
            print('現在掲載を停止している企業です')

        utils.browser_close()