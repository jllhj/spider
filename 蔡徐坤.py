import requests
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}


urls_list = ['https://search.bilibili.com/all?keyword=%E8%94%A1%E5%BE%90%E5%9D%A4&from_source=banner_search&order=click&duration=0&tids_1=0&page={0}'.format(str(i))for i in range(1,51)]

for urls in urls_list:
    print(urls)
    r1 = requests.get(url=urls)

    # print(r1.text)
    soup = BeautifulSoup(r1.text,'html.parser')


    # 标签对象
    content_list = soup.find(name='ul',attrs={'class':'video-contain clearfix'})

    # [标签对象,标签对象]
    video_list = content_list.find_all(name='li',attrs={'class':'video matrix'})
    for item in video_list:
        a1 = item.find(name='a',attrs={'class':'title'})
        a = item.find(name='span',attrs={'class':'so-icon watch-num'})
        up = item.find(name='a',attrs={'class':'up-name'})
        print(a1.text.strip()+'      作者： '+up.text.strip()+'           播放量为'+a.text.strip())
