# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   Request类.py
@Desc:
@Create: 2021/01/31 19:32
"""
from urllib import request
import requests

url = 'https://www.zhihu.com/hot'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56',
    'cookie': '_zap=b3a7f848-46da-4852-94df-68139fc71819; d_c0="AODXNsnvnxKPTgykvVwui56ojAgznZ9w3Gw=|1612750813"; _xsrf=0epCFJLfGuWfJPIiWHMvnprvAvS2SxfH; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1612750818,1612751568,1613462728; captcha_session_v2="2|1:0|10:1613462725|18:captcha_session_v2|28:YzBsbnBoOW4wcTV0OW52N3VxbzA=|09b93eca026d45ee9fd5331e74b7be7307b31f731aad1b3b375986fbef62db54"; SESSIONID=WSdivFOAB61Igcixdsba3dY1Fbh8htjiCBg1RYlUhTy; JOID=UlsSBkJBFyKLcxJ3bUT9vW74nNd4FUBE7gxXPC4KIhfAGHgdEYFtB-55FXFjOV82xp-I97VDv4qTulz7yULfxOM=; osd=UVkWC01CFSaGfBF1aUnyvmz8kdh7F0RJ4Q9VOCMFIRXEFXceE4VgCO17EXxsOl0yy5CL9bFOsImRvlH0ykDbyew=; captcha_ticket_v2="2|1:0|10:1613462758|17:captcha_ticket_v2|228:eyJhcHBpZCI6IjIwMTIwMzEzMTQiLCJyZXQiOjAsInRpY2tldCI6InQwM0pnMnpuaDJhN1ZGSDV3NHB6TkMybGM5dGNMUUlXRDZ2SS03LWM5NTdjb0NuT1FwbnVRa0djUjVLZU5jUHc3eVFIMW50OGQ4Z3BYbnUyYU5MQ0xWZkNpWHRndEJSNFdvR29RSXUxem1ta2tBKiIsInJhbmRzdHIiOiJARWhTIn0=|df8ed5ced9b30187b2a7af38421e3568b220898a615c6019fed61d3a5d135d7e"; z_c0="2|1:0|10:1613462759|4:z_c0|92:Mi4xMzVuWEF3QUFBQUFBNE5jMnllLWZFaVlBQUFCZ0FsVk41OG9ZWVFCcjFXa3g5NjdYVE5DZ09MOE1HQWdMR0RWMHhn|cfac36f315964ee4e9e7b3738e23474bdd08c3557039c5c62b80bf51a83c3877"; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1613462763; KLBRSID=0a401b23e8a71b70de2f4b37f5b4e379|1613462761|1613462724'
}
resp = requests.get(url, headers=headers)
print(resp.text)

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'
# }
# rq = request.Request(url, headers=headers)
# resopnse = request.urlopen(rq)
# print(resopnse.read())
