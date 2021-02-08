# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   实践练习-猫眼票房.py
@Desc:
@Create: 2021/01/31 19:46
"""
# 导入request包
from urllib import request
# 请求URL
url_maoyan = 'http://piaofang.maoyan.com/dashboard-ajax?orderType=0&uuid=17758438371c8-09aa279f4f185-50391c40-384000-17758438371c8&riskLevel=71&optimusCode=10&_token=eJxN0U1rg0AQBuD%2FMudFZz9cd4UchEKx0END2kvIYRNTE4oaVEpL6X%2FvLHanBWEfh3lfZP2CqWmhQgHv5wkqkBlmFgQsM1TSSoXeYIFYGgGn%2FzNnlHMCjtPLHVR7qUonrNaHONnSYK8Ki0IagweRjGRl6IlbDS3BZVluVZ7frmF8DUOX9WH8DEN2Gvu8DfPlOIappW8BCvS7GNCUt1rRbBUmKc8qWZZlWGtWk2SS9KySZVmGxVn5l8UkdCxuwYLFLahZ3IKppfCeVbIsa%2B1TJMNSLExyPl7ZW7wyOsPvuaT3R%2FrPtDpfu4F0fvjYPXdNXd939fZps4HvH8RTdGc%3D'
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'
}

rq = request.Request(url_maoyan, headers=headers)
resopnse = request.urlopen(rq)

movies = resopnse.read().decode('utf-8')

print(movies)
