
#########################################示例一 爬取网站内容#####################################################

"""
import requests
from bs4 import BeautifulSoup

r1 = requests.get(
    url='https://dig.chouti.com/',
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
)


soup = BeautifulSoup(r1.text,'html.parser')

content_list = soup.find(name='div',attrs={'id':'content-list'})

item_list = content_list.find_all(name='div',attrs={'class':'item'})
for item in item_list:
    a = item.find(name='a',attrs={'class':'show-content color-chag'})
    print(a.text.strip())
"""




################################实例二 点赞##################################################
"""
import requests
from bs4 import BeautifulSoup
# 1.查看首页
r1 = requests.get(
    url='https://dig.chouti.com/',
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
)
print(r1.cookies)
# 2. 提交用户名和密码
r2 = requests.post(
    url='https://dig.chouti.com/login',
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'},
    data={
        'phone':'8613121758648',
        'password':'woshiniba',
        'oneMonth':1
    },
    cookies=r1.cookies.get_dict() 设置的反爬虫 需要登入首页 
)



r3 = requests.post(
    url='https://dig.chouti.com/link/vote?linksId=24684771',
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'},
    cookies=r1.cookies.get_dict()
)
print(r3.text)
"""



import requests
from bs4 import BeautifulSoup
# 1. 访问登陆页面，获取 authenticity_token


r1 = requests.get(
    url='https://github.com/login',
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
)

soup = BeautifulSoup(r1.text,features='lxml')
tag = soup.find(name='input',attrs={'name':'authenticity_token'})
authenticity_token = tag.get('value')
c1 = r1.cookies.get_dict()
r1.close()
print(c1)

# 2. 携带authenticity_token和用户名密码等信息，发送用户验证
form_data = {
    "authenticity_token": authenticity_token,
    "utf8": "✓",
    "commit": "Sign in",
    "login": "468867748@qq.com",
    'password': 'vs468867748'
}
