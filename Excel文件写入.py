# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   Excel文件写入.py
@Desc:
@Create: 2021/02/28 15:40
"""
# 导入Excel写入模块
import xlwt
# 随机数
import random
# os库
import os

# 创建一个Workbook对象
workbook = xlwt.Workbook()
# 创建一个Sheet对象
sheet1 = workbook.add_sheet("1班")
# 使用sheet.write方法把数据写入到Sheet下指定行和列中。如果想要在原来workbook对象上添加新的cell，那么需要调用put_cell来添加
# 列名
headers = ['姓名', '语文', '数学', '英语']
for index, header in enumerate(headers):
    sheet1.write(0, index, header)

# 姓名
names = ['张三', '李四', '王五']
for index, name in enumerate(names):
    sheet1.write(index + 1, 0, name)

# 分数
for row in range(1, 4):
    for col in range(1, 4):
        sheet1.write(row, col, random.randint(30, 100))

# 保存成Excel文件
# 如果已经存在，则删除
if os.path.exists("./Excel/成绩表.xls"):
    os.remove("./Excel/成绩表.xls")
workbook.save(r"./Excel/成绩表.xls")
