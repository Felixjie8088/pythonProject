# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   工作周报.py
@Desc:
@Create: 2020/09/22 11:22
"""
import pandas as pd
import matplotlib.pyplot as plot

df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['zhang', 'li', 'wang1'],
    'age': [10, 20, 30]
})

df.set_index('id')
print(df)
# df.to_excel("./File/people.xlsx")
print("Done")

# 读取Excel
student = pd.read_excel("./Excel/Student-1.xlsx")
# sort_values 排序，inplace：False 对当前对象进行更改调整，ascending ：False反序
student.sort_values(by="Name", inplace=False, ascending=False)
# 用bar方法绘制柱状图
plot.bar(student.Name, student.Score, color="blue")
# 设置标题，x轴，y轴
plot.title("student", fontsize=20)
plot.xlabel("Name")
plot.ylabel("Score")

# 如果x轴字数太多，那么则利用xticks方法rotation传参设置旋转角度
plot.xticks(student.Name, rotation="90")
# 布局方式：紧凑布局
plot.tight_layout()
# 最终呈现效果
plot.show()
