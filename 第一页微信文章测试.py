import requests
from urllib.parse import urlencode

from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
import pymongo
client = pymongo.MongoClient('localhost')
db =client['weixin']

keyword = '风景'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.53 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'weixin.sogou.com',
    'Cookie':'IPLOC=CN4414; SUID=B3157D773120910A000000005B7C33AB; SUV=1534866348760671; ld=OZllllllll2tZKW6lllllV8xMtllllllNT1gNZllllGlllllpylll5@@@@@@@@@@; ABTEST=1|1556216306|v1; weixinIndexVisited=1; sct=2; JSESSIONID=aaavFrZ0puyBd8FZcAuPw; PHPSESSID=30cpdp3cp07q2pe9hnbpid0172; SNUID=3C5D363C4A4FCD21C0ED47C84B94B0D2; ppinf=5|1556274821|1557484421|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo2OkhvbmdLaXxjcnQ6MTA6MTU1NjI3NDgyMXxyZWZuaWNrOjY6SG9uZ0tpfHVzZXJpZDo0NDpvOXQybHVFeFc1aC00T1hJY3kwb1pVa0R4THVrQHdlaXhpbi5zb2h1LmNvbXw; pprdig=Mlm-EAK9vM8a9OHxp5u5_qqRCZ17QuftNAVXKDnaFU6cYzIVyCKB8Iy2JTzYvbpFEysTpCAz5wUjLYpIyGMnSANjGMz5K344QFmkvVeXyzL0aGtkcUfr6wBwrpN4Fsorsh8bMdyOmSOwvqc89VJzVPQmZ0Ih-9zOUYjgEKlfCjY; sgid=17-40301873-AVzC3oXcf0o3zp5ic61KQe04; ppmdig=15562748220000005f713048b2cc6aa12f170316fac91a7a'
}
base_url = 'https://weixin.sogou.com/weixin?'

def get_html(url):
    try:
        response = requests.get(url,allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print(302)

    except ConnectionError:
        return get_html(url)

# 解析html
def parse_index(html):
    doc = pq(html)
    items = doc('.news-list li .txt-box h3 a').items()

    for item in items:
        yield item.attr('data-share')

def get_index(keyword,page):
    data = {
        'query':keyword,
        'page':page,
        'type':2
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def get_detail(url): # 微信文章没有反爬虫机制
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        date = doc('#post-date').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title':title,
            'content':content,
            'date':date,
            'nickname':nickname,
            'wechat':wechat
        }
    except XMLSyntaxError:
        return None

def save_to_mongo(data):
    # True 如果查询结果是没有的执行插入 有就更新
    if db['articles'].update({'title':data['title']},{'$set':data},True):
        print('Saved to Mongo',data['title'])
    print('Saved to Mongo Failed',data['title'])


def main():
    html = get_index(keyword,1)
    article_urls = parse_index(html)

    for article_url in article_urls:
        article_html = get_detail(article_url)
        if article_html:
            article_data = parse_detail(article_html)
            print(article_data)
            if article_data:
                save_to_mongo(article_data)


if __name__ == '__main__':
    main()