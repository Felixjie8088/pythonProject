# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:  在lxml中使用xpath语法.py
@Desc:
@Create: 2021/2/22 13:31
"""

from lxml import etree

# 将文件中的内容解析为HTML文档
html = etree.parse('./File/HTML/hello.html')
# # 按字符串序列化HTML文档,并解码
# result = etree.tostring(html).decode('utf-8')

# 获取所有li标签
# result_li = html.xpath('//li')
# for r in result_li:
#     print(etree.tostring(r).decode('utf-8'))
# 获取所有li元素下的所有class属性的值
# result_li_class = html.xpath('//li/@class')
# print(result_li_class)
# 获取li标签下href为www.baidu.com的a标签
# result_li_href = html.xpath('//li/a[@href="www.baidu.com"]')
# for r in result_li_href:
#     print(etree.tostring(r).decode('utf-8'))
# 获取li标签下所有span标签
result_span = html.xpath('//li//span')
for r in result_span:
    print(etree.tostring(r).decode('utf-8'))
# 获取li标签下的a标签里的所有class
result_li_a_class = html.xpath('//li/a/@class')
for r in result_li_a_class:
    print(etree.tostring(r).decode('utf-8'))
# 获取最后一个li的a的href属性对应的值
result_li_last_a_href = html.xpath('//li[last()]/a/@href')
print(result_li_last_a_href)
# 获取倒数第二个li元素的内容
result_li_last_1 = html.xpath('//li[last()-1]/a')
for r in result_li_last_1:
    print(r.text)
# 获取倒数第二个li元素的内容的第二种方式
result_li_last_1_1 = html.xpath('//li[last()-1]/a/text()')
print(result_li_last_1_1)
