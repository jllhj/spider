import requests
from bs4 import BeautifulSoup
import bs4

re_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'referer': 'https://www.taobao.com/',
            'accept-encoding': 'gzip, deflate, b',
        }
response = requests.get('https://s.taobao.com/search?q=%E9%9B%B6%E9%A3%9F&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190511&ie=utf8')
response.encoding = 'utf-8'
print(response.request.url)

# soup = BeautifulSoup(response.text,'html.parser')
# div = soup.find(name='div',attrs={'id':'waterfall'})
#
#
# div_list = div.find_all(name='div')
# for divv in div_list:
#     # print(divv)
#     title = divv.find(name='img')
#     a = divv.find(name='a')
#     img = divv.find(name='img')
#
#     if not a:
#         continue
#     src = img.get('src')
#     print(title.get('title'))
#     print(a.get('href'))
#     # print(img.get('src'))
#     print(src)
#     # 再次发送请求 下载图片
#     # file_name = img.get('src').rsplit('/',maxsplit=1)[1]
#     # ret = requests.get(img.get('src'))
#     # with open (file_name,'wb') as f:
#     #     f.write(ret.content)