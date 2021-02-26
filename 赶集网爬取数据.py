# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:  赶集网爬取数据.py
@Desc:
@Create: 2021/2/26 13:52
"""

# requests请求库
import requests
# re正则表达式库
import re
# time 时间库
import time


class ganji():
    def __init__(self):
        self.page_url = 'http://su.ganji.com/zufang/pn1/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74',
            'Host': 'su.ganji.com',
            'cookie': 'ganji_uuid=9702908012721581993054; ganji_xuuid=4b100698-c9ae-417e-c3b3-fe68ede3a77a.1614318998236; _gl_tracker=%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A50198259394%7D; GANJISESSID=l3oi0or525voh4t36cqgkrdb0d; lg=1; citydomain=su; __utmc=32156897; __utmz=32156897.1614319005.1.1.utmcsr=su.ganji.com|utmccn=(referral)|utmcmd=referral|utmcct=/; gj_footprint=%5B%5B%22%5Cu79df%5Cu623f%22%2C%22http%3A%5C%2F%5C%2Fsu.ganji.com%5C%2Ffang1%5C%2F%22%5D%5D; __utma=32156897.1154073950.1614319005.1614323715.1614329720.3; ganji_login_act=1614331662609; __utmb=32156897.3.10.1614329720'
        }
        self.encoding = 'UTF-8'

    # 根据page_url分批获取每一页的数据，获得每一个详情URL，返回list  re.VERBOSE代表可以在正则表达式中添加注释、re.DOTALL代表可以让正则表达式中的.可以找到换行符（所有字符）
    def get_houses(self):
        house_list = []
        house_info = {}
        html = requests.get(self.page_url, headers=self.headers).text
        div_houses = re.findall(r'''
        <div.+? ershoufang-list".+?<a.+?js-title.+?>(.+?)</a>  # 获取房源标题
        .+?<dd.+?dd-item.+?<span>(.+?)</span>                  # 获取房源户型
        .+?<span.+?<span>(.+?)</span>                          # 获取房源面积
        .+?<span.+?<span>(.+?)</span>                          # 获取房源朝向
        .+?<span.+?<span.+?last.+?>(.+?)</span>                # 获取房源装修类型
        .+?<dd.+?dd-item.+?<span.+?area.+?<a.+?address-eara.+?>(.+?)</a>(.+?)<a.+?<span.+?address-eara.+?>(.+?)</span>      # 获取房源地址
        .+?<div.+?price.+?<span.+?>(.+?)</span><span.+?yue.+?>(.+?)</span>      # 获取房源价格
        ''', html, re.VERBOSE | re.DOTALL)

        # 循环将房源信息取出，字典中
        for house in div_houses:
            # 初始化字典
            house_info = {}
            house_title, house_type, house_size, house_orientation, house_decoration_type, house_address, spacer, house_address_detail, house_price, price_unit = house
            house_info['house_title'] = house_title
            house_info['house_type'] = house_type
            house_info['house_size'] = house_size
            house_info['house_orientation'] = house_orientation
            house_info['house_decoration_type'] = house_decoration_type
            house_info['house_address'] = house_address + spacer.replace('\n', '').strip() + house_address_detail
            house_info['house_price'] = house_price + '' + price_unit
            house_list.append(house_info)

        return house_list

    # 开始运行
    def run(self):
        with(open(r'./Excel/ganjifangyuanxinxi.csv', 'w', encoding='UTF-8')) as f:
            # 分页获取内容
            for i in range(1, 10, 1):
                self.page_url = 'http://su.ganji.com/zufang/pn{}/'.format(i)
                houses = self.get_houses()
                # print(houses)
                for house in houses:
                    f.writelines('''房源标题：{}
                        \n房源户型：{}
                        \n房源面积：{}
                        \n房源朝向：{}
                        \n房源装修类型：{}
                        \n房源详细地址：{}
                        \n房源价格：{}\n\n'''.format(house['house_title']
                                            , house['house_type']
                                            , house['house_size']
                                            , house['house_orientation']
                                            , house['house_decoration_type']
                                            , house['house_address']
                                            , house['house_price']
                                            ))
                print('写入成功！')
                # 间隔1s获取
                time.sleep(5)


if __name__ == '__main__':
    ganji = ganji()
    ganji.run()
