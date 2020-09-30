# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   120年奥运会数据分析.py
@Desc:
@Create: 2020/09/27 11:12
"""
import os
import numpy as np
import pandas as pd
import seaborn as sbn
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from pylab import mpl


# 读取Excel数据、生成图表
def read_Generate_execl(filepath, datasource, orderby, asc, title, x_axis, y_axis, images_path):
    '''
    参数说明
    :param filepath:图片相对路径
    :param datasource:数据源
    :param orderby:排序字段
    :param asc:正序还是倒序
    :param title:图标标题
    :param x_axis:x轴列名
    :param y_asix:y轴列名
    :param images_path:生成图片的路径
    :return:返回成功信息以及生成文件路径
    '''
    # 读取Excel
    data = None
    if not filepath == None:
        data = pd.read_excel(filepath)
    else:
        data = datasource
    # sort_values 排序，inplace：True 对当前对象进行更改调整，ascending ：False反序
    data1 = data.sort_values(by=orderby, inplace=False, ascending=asc)
    # 用bar方法绘制柱状图
    plt.bar(data1.Age, data1.Medal, color="blue")
    # 设置标题，x轴，y轴
    plt.title(title, fontsize=20)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)

    # 如果x轴字数太多，那么则利用xticks方法rotation传参设置旋转角度
    # plt.xticks(data.Age, rotation="90")
    # 布局方式：紧凑布局
    plt.tight_layout()
    # # 最终呈现效果
    # plot.show()
    # 保存数据至图片文件
    plt.savefig(images_path)
    print(f"生成成功,文件路径在：{images_path}")


# 读取文件
# 需要读取的文件的父目录
excel_dirpath = './Excel'
athlete_data = pd.read_csv(os.path.join(excel_dirpath, 'athlete_events.csv'))
regions_data = pd.read_csv(os.path.join(excel_dirpath, 'noc_regions.csv'))

# 返回N行数据
# print(athlete_data.head(5))
# 数据的总体信息，分布趋势，离散度
# print(athlete_data.describe())

# print(athlete_data.info())

# 数据关联merge
merge_left = pd.merge(athlete_data, regions_data, on='NOC', how='left')
# print(merge_left.head(5))

# 只找出年龄和奖牌两列
# df_athlete_data = pd.DataFrame(athlete_data, columns=['Age', 'Medal'])
# 找出所有获得金牌的数据
# df_athlete_data_Medal = df_athlete_data[(df_athlete_data.Medal == 'Gold')]
athlete_goldmedal_data = merge_left[merge_left.Medal == 'Gold']
# 检查数据中每列中是否含有NAN的值，有：True，没有：False
print(athlete_goldmedal_data.isnull().any())
# 检查数据中Age列中是否含有NAN的值，有：True，没有：False
print(athlete_goldmedal_data.Age.isnull().any())
# 将数据中的Age列进行数据过滤，将为NAN的数据过滤掉
athlete_goldmedal_data = athlete_goldmedal_data[np.isfinite(athlete_goldmedal_data['Age'])]
print(athlete_goldmedal_data.head())

# 创建一个画布，画布大小
plt.figure(figsize=(20, 10))
# 紧凑型布局
plt.tight_layout()
sbn.countplot(athlete_goldmedal_data['Age'])
# 字体文件路径
fontpath = './FontSource/SimHei.ttf'
myfont = FontProperties(fname=fontpath)
mpl.rcParams['axes.unicode_minus'] = False
# 加载目标字体(中文显示)
plt.title('金牌数年龄分布', fontproperties=myfont)
# plt.title('Gold')
plt.show()

# read_Generate_execl(filepath=None, datasource=athlete_goldmedal_data, orderby='Age', asc=False, title='Medal-Age', x_axis='Age', y_axis='Medal', images_path='./images/PicExcel/Medal-Age.jpg')

# import cv2
#
# # cv2.IMREAD_COLOR : 默认使用该种标识。加载一张彩色图片，忽视它的透明度。
# # cv2.IMREAD_GRAYSCALE : 加载一张灰度图。
# # cv2.IMREAD_UNCHANGED : 加载图像，包括它的Alpha通道。 友情链接：Alpha通道的概念
# # 提示：如果觉得以上标识太麻烦，可以简单的使用1，0，-1代替。（必须是整数类型）
# img = cv2.imread('./images/AIFaceImg/match_2.jpg', 0)
# print(img)
# img_cv2 = cv2.cvtColor(src=img, code=cv2.COLOR_BAYER_BG2GRAY)
# print(img_cv2)
#
# # 创建窗口并显示图像
# cv2.namedWindow("Image")
# cv2.imshow("Image", img_cv2)
# cv2.waitKey(0)
# # 释放窗口
# cv2.destroyAllWindows()
