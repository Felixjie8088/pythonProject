# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   Excel文件读取.py
@Desc:
@Create: 2021/02/28 12:43
"""
import xlrd

workbook = xlrd.open_workbook('./Excel/渠道数据分析总表.xlsx')

# 获取所有的sheet name  返回一个列表
sheet_name = workbook.sheet_names()
print(sheet_name)
# 根据索引获取sheet对象
sheet_by_index = workbook.sheet_by_index(0)
print(sheet_by_index)
# 根据名称获取sheet对象
sheet_by_name = workbook.sheet_by_name("Sheet")
print(sheet_by_name)
# 获取所有sheet对象
sheets = workbook.sheets()
print(sheets)
# 获取某个sheet中的行数
sheet_row_count = sheet_by_index.nrows
print(sheet_row_count)
# 获取某个sheet中的列数
sheet_col_count = sheet_by_index.ncols
print(sheet_col_count)

"""
Cell   (单元格操作)
"""

# 获取指定行和列的cell对象
cell_obj = sheet_by_index.cell(1, 1)
print('指定行和列的cell对象:', cell_obj)
# 获取指定行的某几列的cell对象
cell_obj_1 = sheet_by_index.row_slice(1, 1, 3)
print('指定行的某几列的cell对象:', cell_obj_1)
# 获取指定列的某几行的cell对象
cell_obj_2 = sheet_by_index.col_slice(1, 1, 3)
print('指定列的某几行的cell对象:', cell_obj_2)
# 获取指定行和列的值
cell_obj_3 = sheet_by_index.cell_value(1, 1)
print('指定行和列的值:', cell_obj_3)
# 获取指定行的某几列的值
cell_obj_4 = sheet_by_index.row_values(1, 1, 3)
print('指定行的某几列的值:', cell_obj_4)
# 获取指定列的某几行的值
cell_obj_5 = sheet_by_index.col_values(1, 1, 3)
print('指定列的某几行的值:', cell_obj_5)


'''
Cell的数据类型
'''

# 文本类型 1
xlrd.XL_CELL_TEXT
# 数值类型 2
xlrd.XL_CELL_NUMBER
# 日期时间类型 3
xlrd.XL_CELL_DATE
# 布尔类型 4
xlrd.XL_CELL_BOOLEAN
# 空白数据类型 0
xlrd.XL_CELL_EMPTY
