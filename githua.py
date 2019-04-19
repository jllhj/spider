import requests
from bs4 import BeautifulSoup

# 1. 访问登陆页面，获取 authenticity_token
i1 = requests.get('https://github.com/login')
soup1 = BeautifulSoup(i1.text, features='lxml')
tag = soup1.find(name='input', attrs={'name': 'authenticity_token'})
authenticity_token = tag.get('value')
# print(authenticity_token)
c1 = i1.cookies.get_dict()
i1.close()

# 2 携带authenticity_token和用户名密码等信息，发送用户验证
i2 = requests.post(url='https://github.com/session',
                   headers={
                       'user-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'},
                   data={
                       'commit':'Sign in',
                       'utf8':'✓',
                       'authenticity_token':authenticity_token,
                       'login':'jllhj',
                       'password':'**4688****',
                   },
                   cookies=c1)
c2 = i2.cookies.get_dict()
c1.update(c2)


i3 = requests.get('https://github.com/settings/emails', cookies=c1)
soup3 = BeautifulSoup(i3.text, features='lxml')
email1 = soup3.find(name='span',attrs={'class':'css-truncate-target'})

print(email1.text)