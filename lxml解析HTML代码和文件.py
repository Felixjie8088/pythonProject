# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:  lxml解析HTML代码和文件.py
@Desc:
@Create: 2021/2/22 10:06
"""
from lxml import etree


h_text = '''
<div>
    <ul>
        <li class="item-0"><a href="link1.html">first item</a></li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-inactive"><a href="link3.html">third item</a></li>
        <li class="item-1"><a href="link4.html">fourth item</a></li>
        <li class="item-0"><a href="link5.html">fifth item</a>
    </ul>
</div>
'''
# 将字符串解析为HTML文档
html = etree.HTML(h_text)
# 按字符串序列化HTML文档,并解码
result = etree.tostring(html).decode('utf-8')

print(result)
