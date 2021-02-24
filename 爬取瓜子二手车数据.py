# -*- coding:utf-8 -*-
"""
@Author: Felix
@File:  爬取瓜子二手车数据.py
@Desc:
@Create: 2021/2/23 14:43
"""
import requests
from lxml import etree


# 根据请求URL、请求头信息获取瓜子二手车详情URL
def get_detail_urls(index_url,headers,encoding='UTF-8'):
    # 返回详情URL
    detail_urls = []
    # 返回图片URL
    img_urls = []
    # 请求获得网页源代码
    html = requests.get(index_url,headers=headers)
    # 解码源代码
    content = html.content.decode(encoding)
    # with open(r'./File/HTML/guazi.html','w',encoding='utf-8') as f:
    #     f.writelines(content)
    # print(content)
    # 先用etree读取返回源代码
    # .decode("unicode_escape").encode('utf-8')
    ehtml = etree.HTML(content)
    # 所有的li标签
    lis = ehtml.xpath('//ul[@class="carlist clearfix js-top"]/li')
    for item in lis:
        detail_url_list = item.xpath('./a/@href')
        img_url_list = item.xpath('.//img/@src')
        detail_url = "https://www.guazi.com" + detail_url_list[0]
        img_url = img_url_list[0]
        # print(etree.tostring(item,encoding=encoding).decode(encoding))
        # print(detail_url)
        # print(img_url)
        detail_urls.append(detail_url)
        img_urls.append(img_url)
    return detail_urls,img_urls


# 瓜子二手车首页
index_url = 'https://www.guazi.com/su/buy/'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74',
    'cookie':'antipas=2I6324LZ2693B0848474gR74; uuid=60050fbd-2c02-4656-c6a4-05068a74b618; cityDomain=su; clueSourceCode=%2A%2300; user_city_id=67; ganji_uuid=8422745155768898953527; sessionid=f10c3542-72b5-4a64-cbd3-1973f308e397; lg=1; Hm_lvt_bf3ee5b290ce731c7a4ce7a617256354=1614062538; close_finance_popup=2021-02-23; lng_lat=120.724156_31.264922; gps_type=1; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%2260050fbd-2c02-4656-c6a4-05068a74b618%22%2C%22ca_city%22%3A%22su%22%2C%22sessionid%22%3A%22f10c3542-72b5-4a64-cbd3-1973f308e397%22%7D; preTime=%7B%22last%22%3A1614062581%2C%22this%22%3A1614062535%2C%22pre%22%3A1614062535%7D; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A52994690827%7D; Hm_lpvt_bf3ee5b290ce731c7a4ce7a617256354=1614062595'
}

# 获取详情页中车辆型号名称、公里数、排量、变速箱类型
def get_detail_info(detail_url,headers,encoding='UTF-8'):
    html = requests.get(detail_url,headers=headers)
    content = html.content.decode(encoding)
    ehtml = etree.HTML(content)
    # 车辆型号名称
    detail_info_title = ehtml.xpath('//div[@class="product-textbox"]/h1/text()')[0]
    detail_info_title = detail_info_title.replace(r'/r/n','').strip()
    #包含公里数、排量、变速箱类型的span
    detail_info_span = ehtml.xpath('//div[@class="product-textbox"]/ul//span/text()')
    # 公里数
    detail_info_span_km = detail_info_span[2]
    # 排量
    detail_info_span_displacement = detail_info_span[3]
    # 变速箱类型
    detail_info_span_speedbox = detail_info_span[4]
    # print('车辆信息：',detail_info_span)
    # 车辆信息字典
    infos = {}
    infos['title'] = detail_info_title
    infos['km'] = detail_info_span_km
    infos['displacement'] = detail_info_span_displacement
    infos['speedbox'] = detail_info_span_speedbox
    print(infos)
    # print('车辆型号名称：',detail_info_title)
    # print('公里数：',detail_info_span_km)
    # print('排量：',detail_info_span_displacement)
    # print('变速箱类型：',detail_info_span_speedbox)

# 获取详情URL、图片URL
detail_url_list,img_url_list = get_detail_urls(index_url,headers)
print(detail_url_list)
print(img_url_list)
# 循环获取详情页信息
for detail_url in detail_url_list:
    get_detail_info(detail_url,headers=headers)

