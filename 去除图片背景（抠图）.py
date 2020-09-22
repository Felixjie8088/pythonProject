# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   去除图片背景（抠图）.py
@Desc:
@Create: 2020/09/21 14:52
"""
import removebg

rmbg = removebg.RemoveBg(api_key="TSoFQ21EhJF634VtkEuLWX92", error_log_file="./File/Error_log_rmbg.txt")
rmbg.remove_background_from_img_file("./images/AIFaceImg/match_1.jpg")
