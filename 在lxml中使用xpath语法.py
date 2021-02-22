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
result_li = html.xpath('//li')
for r in result_li:
    print(etree.tostring(r).decode('utf-8'))
# 获取所有li元素下的所有class属性的值
result_li = html.xpath('//li')
print(etree.tostring(result_li[0]).decode('utf-8'))
# 获取li标签下href为www.baidu.com的a标签

# 获取li标签下所有span标签

# 获取li标签下的a标签里的所有class

# 获取最后一个li的a的href属性对应的值

# 获取倒数第二个li元素的内容

# 获取倒数第二个li元素的内容的第二种方式