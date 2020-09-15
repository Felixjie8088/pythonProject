# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   Excel文件操作.py
@Desc:
@Create: 2020/09/04 11:42
"""
from openpyxl import workbook

# 创建一个工作簿
wb = workbook()
# 定位当前sheet页
ws = wb.active
ws.title = '练习'
# 创建sheet
ws2 = wb.create_sheet('练习2')
# 查看当前工作簿的sheetnames
