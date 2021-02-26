# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:  json文件存储.py
@Desc:
@Create: 2021/2/26 18:03
"""
import json

books = [
    {
        'name': '三国演义',
        'price': 20.00
    },
    {
        'name': '红楼梦',
        'price': 52.00
    },
    {
        'name': '水浒传',
        'price': 38.99
    }
]
# 直接转换成json对象
result = json.dumps(books, ensure_ascii=False)
print(result)
print(type(result))

# dumps将转换完成的json对象存储到文件中
fp = open('./File/books.json', 'w', encoding='UTF-8')
json.dump(books, fp, ensure_ascii=False)
fp.close()

# json转换成Python对象
json_str = '[{"name": "三国演义", "price": 20.0}, {"name": "红楼梦", "price": 52.0}, {"name": "水浒传", "price": 38.99}]'
result_1 = json.loads(json_str)
print(result_1)
print(type(result_1))


with(open('./File/books.json', 'r', encoding='UTF-8')) as fp_json:
    resu = json.load(fp_json)
    print(resu)
    print(type(resu))