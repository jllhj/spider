import requests
from urllib.parse import urlencode

from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
import pymongo
client = pymongo.MongoClient('localhost')
db =client['weixin']
base_url = 'https://weixin.sogou.com/weixin?'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.53 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'weixin.sogou.com',
    'Cookie': 'IPLOC=CN4414; SUID=B3157D773120910A000000005B7C33AB; SUV=1534866348760671; ld=OZllllllll2tZKW6lllllV8xMtllllllNT1gNZllllGlllllpylll5@@@@@@@@@@; ABTEST=1|1556216306|v1; weixinIndexVisited=1; sct=2; JSESSIONID=aaavFrZ0puyBd8FZcAuPw; ppinf=5|1556216388|1557425988|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo2OkhvbmdLaXxjcnQ6MTA6MTU1NjIxNjM4OHxyZWZuaWNrOjY6SG9uZ0tpfHVzZXJpZDo0NDpvOXQybHVFeFc1aC00T1hJY3kwb1pVa0R4THVrQHdlaXhpbi5zb2h1LmNvbXw; pprdig=f5_JCx0jui6L2f9L-Sa_V9faAujlEAgXkIDx4KaMvriTgqtj83ZT_bgL_-oMfNDraTZ3fBFEUvj3212VFeDQV-I46r_r_QvSNXKTcjAYPVyUMEdHOmik6kgM7fbER7oH8XRWbPxEMcIUA-4i_MqlvD5TYQML2yZD_EjOCVfFpDE; sgid=17-40301873-AVzBibkQYEHJwia2qRYAPk29M; ppmdig=155621638800000028c8e1046083da7122b6cc42f5e648e3; PHPSESSID=30cpdp3cp07q2pe9hnbpid0172; SNUID=CDAEC7CDBABF3EE75C44ABDFBA26BCC5; seccodeRight=success; successCount=1|Thu, 25 Apr 2019 18:27:18 GMT; refresh=1'
}
keyword = '风景'
proxy_pool_url = 'http://127.0.0.1:5000/get'
max_count = 5
proxy = None

def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def get_html(url,count=1):
    print('Crawling',url)
    print('Trying Count',count)
    global proxy
    if count >= max_count:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy: # 如果有代理
            proxies = {
                'http':'http://'+proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers,proxies=proxies)
        # 302会自动处理跳转 加了allow_redirects=False就不会自动
        else:
            response = requests.get(url,allow_redirects=False,headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy 被封 设置换代理
            print(302)
            proxy = get_proxy()
            if proxy:
                print('Using Proxy',proxy)
                count += 1
                return get_html(url, count)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occurred',e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url,count)


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

# 解析html
def parse_index(html):
    doc = pq(html)
    items = doc('.news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

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

def get_detail(url): # 微信文章没有反爬虫机制
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def save_to_mongo(data):
    # True 如果查询结果是没有的执行插入 有就更新
    if db['articles'].update({'title':data['title']},{'$set':data},True):
        print('Saved to Mongo',data['title'])
    else:
        print('Saved to Mongo Failed',data['title'])

def main():
    for page in range(1,101):
        html = get_index(keyword,page)
        if html:
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