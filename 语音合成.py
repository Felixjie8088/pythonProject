# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   语音合成.py
@Desc:
@Create: 2020/09/13 22:31
"""
from aip import AipSpeech

APP_ID = '123456PYTHON'
API_KEY = '4E1BG9lTnlSeIf1NQFlrSq6h'
SECRET_KEY = '544ca4657ba8002e3dea3ac2f5fdd241'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
print(client)

s = '你好啊，我叫Felix，你叫什么,小宝贝'
speak = client.synthesis(s, 'zh', 1, {
    'vol': 7,  # 音量，取值0-15，默认5位中音量
    'per': 0,
    'spd': 6,  # 语速，取值0-9，默认5位中语速
    'pit': 6  # 音调，取值0-9，默认5位中音调
})
print(speak)
instance = isinstance(speak, dict)
print(instance)

if not isinstance(speak, dict):
    with open('./Audio/myspeech.mp3', 'wb') as f:
        f.write(speak)
