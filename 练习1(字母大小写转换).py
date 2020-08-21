# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   练习1(字母大小写转换).py
@Desc:
@Create: 2020/08/12 14:09
"""

# 用户输入的字母，如果输入的字母ASCII码>=97&&《=122说明是小写字母,如果是65-90之间的说明是大写字母，其他的说明填写错误
letter_input = input('请输入需要转换的字母串:')
# 返回列表
lst_letter_output = []
for i in letter_input:
    ascii_letter = ord(i)
    if ascii_letter > 122 or ascii_letter < 65 or (ascii_letter > 90 and ascii_letter < 97):
        print('填写错误，请输入正确的字母！')
        break

    '''
    写法一
    '''
    # # 小写字母转大写
    # if ascii_letter >= 97 and ascii_letter <= 122:
    #     ascii_letter -= 32
    #     print('转换后的字母是：', chr(ascii_letter))
    # # 大写字母转小写
    # elif ascii_letter >= 65 and ascii_letter <= 90:
    #     ascii_letter += 32
    #     print('转换后的字母是：', chr(ascii_letter))

    '''
    写法二
    '''
    # 小写字母转大写
    if i.islower():
        lst_letter_output.append(i.upper())
    # 大写字母转小写
    elif i.isupper():
        lst_letter_output.append(i.lower())

print('转换后的字母串是：', ''.join(lst_letter_output))
