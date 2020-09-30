# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:   Python实现办公自动化.py
@Desc:   实现功能：
         # 1.Excel自动化
         # 2.邮件发送自动化
         # 3.邮件接收自动化
         # 4.发送短信通知
@Create: 2020/09/29 15:09
"""
import pandas as pd
# 发送邮件
import smtplib
# 构造邮件格式和内容
import email
# 负责构造文本
from email.mime.text import MIMEText
# 负责构造图片
from email.mime.image import MIMEImage
# 负责将多个对象聚合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header

# SMTP服务器，这里使用126邮箱
# mail_host = 'smtp.126.com'
mail_host = 'smtp.qq.com'
# 发件人邮箱
# mail_sender = 'felixjie@126.com'
mail_sender = '992633726@qq.com'
# 邮箱授权码
# mail_license = 'NHOCYSKIAAHOJKRL'
mail_license = 'mockyishlwlqbcda'
# 收件人邮箱
# mail_receivers = ['992633726@qq.com']
mail_receivers = ['felixjie@126.com', '1501393222@qq.com']
# 构建MIMEMultipart对象代表邮件本身，可以往里面添加文本、图片、附件等
mm = MIMEMultipart('related')
# 邮件主题
subject_content = """Python邮件发送测试"""
# 设置发送者，注意严格遵守格式，里面邮箱为发件人邮箱
mm['From'] = f'sender_name<{mail_sender}>'
# 设置接受者，注意严格遵守格式，里面邮箱为接收者邮箱
for index, receiver in enumerate(mail_receivers):
    mm['To'] = f'receiver_{index + 1}_name<{receiver}>'
# 设置邮件主题
mm['subject'] = Header(subject_content, 'utf-8')

# 邮件正文内容
body_content = """你好，这是一个Python测试邮件！"""
# 构造文本，参数1：正文内容，参数2：文本格式，参数3：编码方式
message_text = MIMEText(body_content, 'plain', 'utf-8')
# 向MIMEMultipart对象中添加文本对象
mm.attach(message_text)

# 二进制读取图片
image_data = open('./images/AIFaceImg/match_2.jpg', 'rb')
# 设置读取获取的二进制数据
message_image = MIMEImage(image_data.read())
# 关闭刚才打开的文件
image_data.close()
# 添加图片文件到邮件信息当中去
mm.attach(message_image)

# 构造附件
attachment = MIMEText(open('./Excel/Student-1.xlsx', 'rb').read(), 'base64', 'utf-8')
# 设置附件信息
attachment['Content-Disposition'] = 'attachment; filename="Student-1.xlsx"'
# 添加附件到邮件信息当中去
mm.attach(attachment)

try:
    # 创建SMTP对象
    stp = smtplib.SMTP()
    # 设置发件人邮箱的域名和端口，端口地址为25
    stp.connect(mail_host, 25)
    # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
    stp.set_debuglevel(1)
    # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
    stp.login(mail_sender, mail_license)
    # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
    stp.sendmail(mail_sender, mail_receivers, mm.as_string())
    print('邮件发送成功，请注意查收！')
    # 关闭SMTP对象
    stp.quit()
except Exception as e:
    print(f'发送失败，错误信息{str(e)}')

# # 读取文件
# data = pd.read_excel("./Excel/渠道数据分析总表.xlsx")
# names = {
#     '翟丹': '992633726@qq.com',
#     '陈文': '992633726@qq.com'
# }
#
# for name, email in names.items():
#     data_name = data.loc[data['负责人'] == name]
#     filepath_name = f'./Excel/{name}.xlsx'
#     writer = pd.ExcelWriter(filepath_name)
#     data_name.to_excel(writer, name)
#     writer.save()
#     # 邮件处理
#     if email:
#         pass
# data_name = data.loc[data.groupby(data['负责人'])]
# print(data_name.head())
# 过滤数据
# df = data.loc[data['负责人'] == name]
