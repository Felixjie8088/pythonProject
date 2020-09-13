# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   爬虫小练习.py
@Desc:
@Create: 2020/09/13 23:26
"""
import re
import json
from datetime import datetime
import pandas as pd
import requests

request_url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
page = requests.get(request_url).content.decode("utf-8")
regexp = "<script id = \"getTimelineService2\">([^<]+)"

resp = re.findall(regexp, page)
# print(page)
print(resp)
print(regexp)
print(resp[0])
data = resp[0][44:-11]
dicts = json.loads(data)
print(dicts)
for row in dicts:
    for key in row:
        if key in ["createTime", "mondifyTime"]:
            row[key] = datetime.fromtimestamp(row[key] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        print(key, ":", row[key], end=" ")
    print("\n")

df = pd.DataFrame(dicts)
df.to_csv("./Excel/ncovl.csv", mode="a")
