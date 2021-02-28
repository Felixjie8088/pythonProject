# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   Excel编辑操作.py
@Desc:
@Create: 2021/02/28 17:50
"""
import xlrd
import xlwt
from functools import reduce

workbook_score = xlrd.open_workbook('./Excel/成绩表.xls')
sheet_1class = workbook_score.sheet_by_index(0)

# 添加总分列
sheet_1class.put_cell(0, sheet_1class.ncols, xlrd.XL_CELL_TEXT, "总分", None)
# 添加每个学生的平均分列
sheet_1class.put_cell(0, sheet_1class.ncols, xlrd.XL_CELL_TEXT, "平均分", None)

# 循环找出每个学生的各项成绩，并计算总分插入到总分单元格,计算平均分填充到平均分列
for row in range(1, sheet_1class.nrows):
    score_list = sheet_1class.row_values(row, 1, 4)
    # print(score_list)
    # 列表中元素求和
    total = sum(score_list)
    count = len(score_list)
    avg = total / count
    # print(total)
    # print(count)
    # print(avg)
    # print(sum(score_list))
    # print(reduce(lambda x, y: x + y, score_list))
    # 把值填充至总分单元格
    sheet_1class.put_cell(row, 4, xlrd.XL_CELL_NUMBER, total, None)
    # 把值填充至总分单元格
    sheet_1class.put_cell(row, 5, xlrd.XL_CELL_NUMBER, avg, None)
ncols = sheet_1class.ncols
nrows = sheet_1class.nrows
# print(sheet_1class.ncols)
# print(sheet_1class.nrows)
# print(type(sheet_1class.nrows))
# 计算总平均分列
for col in range(1, ncols):
    score_list_1 = sheet_1class.col_values(col, 1, nrows)
    # 列表中元素求和
    print(score_list_1)
    total = sum(score_list_1)
    count = len(score_list_1)
    avg = total / count
    # print(total)
    # print(count)
    # print(avg)
    # 把值填充至总分单元格
    sheet_1class.put_cell(nrows, col, xlrd.XL_CELL_NUMBER, avg, None)

# 添加每个科目的平均分列  在这添加，可避免之前获取数据会获取到空的值
sheet_1class.put_cell(nrows, 0, xlrd.XL_CELL_TEXT, "科目平均分", None)

# 创建一个新的Excel，将上面的数据保存到新的Excel中
workbook_score_write = xlwt.Workbook()
wsheet = workbook_score_write.add_sheet("Sheet")
nrows = sheet_1class.nrows
ncols = sheet_1class.ncols

for row in range(0, nrows):
    for col in range(0, ncols):
        wsheet.write(row, col, sheet_1class.cell_value(row, col))

workbook_score_write.save("./Excel/成绩表_NEW.xls")
