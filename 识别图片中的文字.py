# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   识别图片中的文字.py
@Desc:
@Create: 2020/07/24 13:13
"""
import pytesseract
from PIL import Image

__author__ = 'admin'

img = Image.open(r'D:\Felix\学习\PyPro\pythonProject\images\picToWord\图片转文字_09.jpg')
# img = Image.open(r'D:\Felix\pythonProject\images\picToWord\图片转文字_09.jpg')
print(pytesseract.image_to_string(img, lang='chi_sim'))
