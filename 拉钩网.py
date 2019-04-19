import requests
import re
# 第一步：访问登陆页,拿到X_Anti_Forge_Token，X_Anti_Forge_Code
# 1、请求url:https://passport.lagou.com/login/login.html
# 2、请求方法:GET
# 3、请求头:
#    User-agent
r1 = requests.get('https://passport.lagou.com/login/login.html',
                  headers={
                      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                  },
                  )
X_Anti_Forge_Token = re.findall("X_Anti_Forge_Token = '(.*?)'", r1.text, re.S)[0]
X_Anti_Forge_Code = re.findall("X_Anti_Forge_Code = '(.*?)'", r1.text, re.S)[0]
print(X_Anti_Forge_Token, X_Anti_Forge_Code)


r2 = requests.get('https://passport.lagou.com/login/login.json',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Referer': 'https://passport.lagou.com/login/login.html', # 上一次请求的地址是什么
        'X-Anit-Forge-Code': X_Anti_Forge_Code,
        'X-Anit-Forge-Token': X_Anti_Forge_Token,

    },
    data={
        "isValidate": True,
        'username': '15131255089',
        'password': 'ab18d270d7126ea65915c50288c22c0d',
        'request_form_verifyCode': '',
        'submit': ''
    },
    cookies=r1.cookies.get_dict()

)
print(r2.text)