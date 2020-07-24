# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   AI人脸识别.py
@Desc:
@Create: 2020/07/23 18:22
"""
# 导入所需的包
import os
import face_recognition

# 创建一个图片的List集合
list_img = os.listdir('images')
# 加载图片
img_to_be_matched = face_recognition.load_image_file("my_image.jpg")
# 解析图片信息
img_to_be_matched_encoded = face_recognition.face_encodings(img_to_be_matched)[0]

for img in list_img:
    # 加载图片
    current_img = face_recognition.load_image_file("images/" + img)
    # 解析图片信息
    current_img_encode = face_recognition.face_encodings(current_img)[0]
    # 判断是否匹配上
    match_result = face_recognition.compare_faces([img_to_be_matched_encoded], current_img_encode)
    if match_result[0]:
        print("Matched:" + img)
    else:
        print("Not Matched:" + img)
