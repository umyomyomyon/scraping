import utils
import os
import MySQLdb
import time
import selenium
import settings
from selenium import webdriver

USER_ID = settings.USER_ID
PASS_WORD = settings.PASS_WORD
TIME_TO_WAIT = 3
NUMBER_OF_COMPANY = 5#16412
URL_CSV_PATH = settings.URL_CSV_PATH
DB_UNIX_SOCKET = settings.DB_UNIX_SOCKET
DB_HOST = settings.DB_HOST
DB_USER = settings.DB_USER
DB_PASS_WORD = settings.DB_PASS_WORD
DB_NAME = settings.DB_NAME

if __name__ == '__main__':
    utils.login(USER_ID, PASS_WORD)
    utils.set_wait_time(TIME_TO_WAIT)
    utils.check_current_url()

    #csvが存在していなかったら、urlを全て配列に格納し、csvとしてエクスポートする
    if os.path.exists(URL_CSV_PATH) == False:
        utils.move_to_company_list()
        url_arr = utils.get_url(NUMBER_OF_COMPANY)
        utils.export_csv(url_arr, URL_CSV_PATH)
        utils.browser_close()
    else:
        #csvが存在していたら、csvを読み込んでurl_arrに格納する
        url_arr = utils.import_csv(URL_CSV_PATH)

    #DB接続
    connector = MySQLdb.connect(
        unix_socket = DB_UNIX_SOCKET,
        host=DB_HOST, user=DB_USER, passwd=DB_PASS_WORD, db=DB_NAME
    )
    corsor = connector.cursor()

    total_time = 0
    number_of_data = 0
    not_exist = 0
    for i in range(len(url_arr)):
        start = time.time()
        utils.open_new_page(url_arr[i])

        try:
            utils.content_scraping(corsor, connector)
        except selenium.common.exceptions.NoSuchElementException as e:
            print('現在掲載を停止している企業です')
            not_exist += 1

        utils.browser_close()
        processing_time = time.time() - start
        print(i)
        print('処理時間:{0}(s)'.format(processing_time))
        total_time += processing_time
        number_of_data += 1

    average_processing_time = total_time / number_of_data
    print("平均処理時間:{0}(s)".format(average_processing_time))
    print("掲載を停止している企業数:{0}".format(not_exist))