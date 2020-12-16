import re
import os
import csv
import json
import time
import random
import requests

# 生成Session对象，用于保存Cookie
s = requests.Session()
#构建动态ip池
ip_txt_url = 'C:/Users/57194/Desktop/社交媒体/spider/ip_list_space.txt'
ip_lists = []
idx = 0
with open(ip_txt_url, 'r') as f:
    lines = f.readlines()
    for line in lines:
        ip_lists.append(line)
ip_list = ip_lists[0].split(' ')

def get_ip_proxy(ip_list):
    IP = ''.join(str(random.choice(ip_list)).strip())
    proxy = {'http':IP}
    return proxy

# def RandomUserAgent(headers_list,mid):
#     header = {'User-Agent': random.choice(headers_list),
#         # ':authority': 'm.weibo.cn',
#         # ':method': 'GET',
#         # ':scheme': 'https',
#         # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         # 'accept-encoding': 'gzip, deflate, br',
#         # 'accept-language': 'zh-CN,zh;q=0.9',
#         # 'cache-control': 'max-age=0',
#         # 'sec-fetch-dest': 'empty',
#         # 'sec-fetch-mode': 'same-origin',
#         # 'sec-fetch-site': 'same-origin',
#         # 'upgrade-insecure-requests': '1'
#         'accept': 'application/json, text/plain, */*',
#         'accept-encoding': 'gzip, deflate, br',
#         'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
#         'cache-control': 'max-age=0',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'same-origin',
#         'sec-fetch-site': 'same-origin',
#         'upgrade-insecure-requests': '1',
#         'referer': 'https://m.weibo.cn/detail/'+str(mid),
#        }
#     return header
def RandomUserAgent(headers_list, weibo_id):
    header = {'User-Agent': random.choice(headers_list),
              # ':authority': 'm.weibo.cn',
              # ':method': 'GET',
              # ':scheme': 'https',
              'Referer': 'https://m.weibo.cn/detail/' + str(weibo_id),
              'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'accept-encoding': 'gzip, deflate, br',
              'accept-language': 'zh-CN,zh;q=0.9',
              'cache-control': 'max-age=0',
              'sec-fetch-dest': 'empty',
              'sec-fetch-mode': 'same-origin',
              'sec-fetch-site': 'same-origin',
              'upgrade-insecure-requests': '1'
              }
    return header
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.36 Safari/525.19',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14',
    'Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
]   
def get_url(weibo_id, max_id):
    # max_id: 1:表示是第一页，0:表示已经到最后一页，其他数字：跳转到下一页
    if(max_id == 1):
        url = 'https://m.weibo.cn/comments/hotflow?id='+ str(weibo_id) + '&mid='+ str(weibo_id) +'&max_id_type=0'
    elif(max_id != 0):
        url = 'https://m.weibo.cn/comments/hotflow?id='+ str(weibo_id) + '&mid='+ str(weibo_id) +'&max_id=' + str(max_id) + '&max_id_type=0'
    else:
        print('max_id:' + str(max_id) + ', 爬完了哦~')
        # 'https://m.weibo.cn/comments/hotflow?id=4502282747842178&mid=4502282747842178&max_id=139256469103475&max_id_type=0'
    print(url)
    return url

def spider_comment(comment_url,weibo_id,output,uid):
    
    kv = RandomUserAgent(my_headers,weibo_id)
    try:
        proxy = get_ip_proxy(ip_list)
        print(proxy)
        r = s.get(url=comment_url, headers=kv,proxies=proxy)
        r.raise_for_status()
        print(r.status_code)
    except:
        print('爬取失败')
        return
    print(r.text)
    r_json = json.loads(r.text)
    try:
        outjson = r_json['data']['data']
        print(len(outjson))
    except:
        print("评论无法显示")
        return
    with open(output,'a',encoding='utf-8') as file:
        for i in range(len(outjson)):
            id = outjson[i]["id"]
            date = outjson[i]["created_at"]
            fromid = outjson[i]["user"]["id"]
            text = outjson[i]["text"]
            reply_dict = {"uid":uid,"weibo_id":weibo_id, "reply_id":id, "date":date, "reply_fromid":fromid, "text":text}
            file.write(json.dumps(reply_dict,ensure_ascii=False,separators=(',',':')))
            file.write('\n')
        print(str(weibo_id)+'comment.json保存成功')
    max_id = r_json['data']['max_id']
    print(max_id)
    time.sleep(random.randint(3, 6))
    return max_id

#patch_spider_comment控制翻页,max_id返回页数
output = 'C:/Users/57194/Desktop/社交媒体/spider/mongo/replies1.json'
def patch_spider_comment(weibo_id,max_id,output,uid):
    comment_url = get_url(weibo_id,max_id)
    max_id = spider_comment(comment_url,weibo_id,output,uid)
    if(max_id!=0):
        patch_spider_comment(weibo_id,max_id,output,uid)
    else:
        print('爬完啦')

if __name__ == '__main__':
    #要爬评论的微博id
    weibo_id = '4502282747842178'
    patch_spider_comment(weibo_id,1,output,uid)
