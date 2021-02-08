# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   实践练习-猫眼票房.py
@Desc:
@Create: 2021/01/31 19:46
"""
# 导入request包
from urllib import request

'''
URL请求
'''


def f_request(url, User_Agent):
    # 请求头
    headers = {
        'User-Agent': User_Agent
    }

    rq = request.Request(url, headers=headers)
    resopnse = request.urlopen(rq)

    readData = resopnse.read().decode('utf-8')
    return readData


# data = f_request('https://www.biedoul.com/index/4253/', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56')
#
# print(data)

# ProxyHandler处理器
# 没有使用代理
data = f_request('http://httpbin.org/ip', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56')
print(data)

# 使用代理
# 步骤
# url = 'http://httpbin.org/ip'
# # 1. 使用ProxyHandler，传入代理构建一个handler
# handler = request.ProxyHandler({'http': '182.46.206.213:9999'})
# # 2. 使用上面创建的handler构建一个opener
# opener = request.build_opener(handler)
# # 3. 使用opener去发送一个请求
# resp = opener.open(url)
# print(resp.read())


'''知乎模拟登陆'''
url_zhihu = 'https://www.zhihu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56',
    'cookie': '_zap=8991146f-8760-4490-b13d-f3e44eb30879; d_c0="AEDd1UcDThGPTnQfmzmSSnAfREmuR57i9n8=|1590073127"; _ga=GA1.2.1383104613.1590073129; _xsrf=sB7XErMNKK1OvgvoDTK4Q61LS2RPJ49u; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1612099905; SESSIONID=xYRwigmFH9THLPHIzYx1JNjTscC4eac2Iw3A9VaAj4G; JOID=WlkSAkwCNoWUqgkZcwswEarqsoJtc2nR5cxncjNFBtfa4FZYPEiHk_2sBhlzxSkDWs3tH452dqGETHDKSvUeSt8=; osd=V18cAkwPMIuUqgQffQswHKzksoJgdWfR5cFhfDNFC9HU4FZVOkaHk_CqCBlzyC8NWs3gGYB2dqyCQnDKR_MQSt8=; capsion_ticket="2|1:0|10:1612100193|14:capsion_ticket|44:MmEzYTEwOGQ1YWI2NGI2OWE3ZDRkY2Q2MzUyYzY5MGY=|73322a7fd595a4d7cdad3e6b401805a78058a80f6c7f978f4af4284963c0d2e2"; z_c0="2|1:0|10:1612100206|4:z_c0|92:Mi4xMzVuWEF3QUFBQUFBUU4zVlJ3Tk9FU1lBQUFCZ0FsVk5iZ0FFWVFCVkpFY3pCRkxVV0dmc2tjbHJZVTZRRDRQSE1R|f9a5ff9bb8d702a1ee9491b64cb01f9e87aba0896f6d353f43d2cd63e4537a47"; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1612100204; KLBRSID=3d7feb8a094c905a519e532f6843365f|1612100208|1612099908'
}

rq = request.Request(url_zhihu, headers=headers)
resopnse = request.urlopen(rq)
readData = resopnse.read().decode('utf-8')
print(readData)
