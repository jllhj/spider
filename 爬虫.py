import requests
from bs4 import BeautifulSoup
import bs4

response = requests.get('https://www.d****.net/')
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text,'html.parser')
div = soup.find(name='div',attrs={'id':'waterfall'})


div_list = div.find_all(name='div')
for divv in div_list:
    # print(divv)
    title = divv.find(name='img')
    a = divv.find(name='a')
    img = divv.find(name='img')

    if not a:
        continue
    src = img.get('src')
    print(title.get('title'))
    print(a.get('href'))
    # print(img.get('src'))
    print(src)
    # 再次发送请求 下载图片
    # file_name = img.get('src').rsplit('/',maxsplit=1)[1]
    # ret = requests.get(img.get('src'))
    # with open (file_name,'wb') as f:
    #     f.write(ret.content)