import re
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'product2'
KEYWORD = '美食'
PAGE_NUM=5            #爬取页数

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

browser = webdriver.Chrome()
wait=WebDriverWait(browser, 10)

def search():
    print('正在搜素...')
    try:
        browser.get('https://s.taobao.com/search?q=%E7%BE%8E%E9%A3%9F&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=-30&p4ppushleft=%2C44&ntoffset=-30&fs=1&filter_tianmao=tmall&s=0')
        page_num=PAGE_NUM
        get_products()      # 获取页面详情
        return page_num
    except TimeoutException:
        return search()

# 获取下页
def next_page(page_number):
    print('正在翻页%s', page_number)
    time.sleep(3)
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

# 解析页面
def get_products():
    # 判断元素是否已经加载下来
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html=browser.page_source
    doc=pq(html)
    items=doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product={
            # 'image': item.find('.pic .img').attr('src'),
            'title': item.find('.title').text(),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'location': item.find('.location').text(),
            'shop': item.find('.shop').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MongoDB成功',result)
    except Exception:
        print('存储到MongoDB失败',result)

def main():
    try:
        page_num=search()
        for i in range(2,page_num+1):
            next_page(i)
    except Exception:
        print('出错啦')
    finally:
        browser.close()

if __name__ == '__main__':
    main()