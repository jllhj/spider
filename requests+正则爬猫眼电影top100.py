import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):

    results = re.findall('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>',html,re.S)
    for result in results:
        yield {
            'index':result[0],
            'img':result[1],
            'title':result[2],
            'actors':result[3].strip()[3:],
            'time':result[4].strip()[5:],
            'score':result[5]+result[6]
        }



def write_to_file(connect):
    f = open('result.txt', 'a+', encoding='utf-8')
    f.write(json.dumps(connect,ensure_ascii=False)+'\n') # 显示中文 json是因为wirte是要字符串格式
    f.close()


def main(offset):
    url = 'https://maoyan.com/board/4?offset=%s'%str(offset)
    print(url)
    html = get_one_page(url)

    for item in parse_one_page(html):
        # print(item)
        write_to_file(item)



if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])