from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time

browser = webdriver.Chrome()
wait=WebDriverWait(browser, 10)
PAGE_NUM = 5

def search():
    try:
        browser.get('https://www.taobao.com/')
        page_num = PAGE_NUM
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button'))
        )
        input.send_keys('零食')
        submit.click()
        get_product()
        return page_num

    except TimeoutException:
        search()

def next_page(page_number):
    print('正在翻页%s', page_number)
    time.sleep(3)
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span')))
        get_product()

    except TimeoutException:
        next_page(page_number)


def get_product():
    # 判断元素是否已经加载下来
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
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