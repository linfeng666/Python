# _*_ coding:utf-8 _*_

import requests
from lxml import etree
import urllib2


# 代理ip下载工具类
class daili_proxy(object):
    """爬取代理ip"""
    def __init__(self):
        self.base_url = 'http://www.xicidaili.com/nn/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        }

        # ip
        self.ip_xpath = '//tr/td[2]/text()'
        # 端口
        self.port_xpath = '//tr/td[3]/text()'
        # 协议
        self.http_xpath = '//tr/td[6]/text()'

    # 发送请求
    def send_request(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            data = response.content
            return data
        except Exception, err:
            print err

    # 数据筛选解析的方法
    def analysis_data(self, data):
        # 1.转类型
        html_data = etree.HTML(data)

        # 2.xpath
        http_data = html_data.xpath(self.http_xpath)
        ip_data = html_data.xpath(self.ip_xpath)
        port_data = html_data.xpath(self.port_xpath)

        count = 0
        proxy_list = []
        len_num = len(http_data) + 1
        for i in range(1,len_num):
            new_dict = {}
            key = http_data[count]
            val = '%s:%s'% (ip_data[count],port_data[count])
            new_dict['%s' % key] = '%s' % val
            ip_temp = new_dict
            proxy_list.append(ip_temp)
            count += 1
        return proxy_list, count

    # 调度方法
    def run(self):
        # 所有http代理ip列表
        proxy_list = []
        count = 0
        # 爬取的页数
        page = int(raw_input("请输入需要爬取的页数"))
        print '正在获取"西刺高匿代理ip"'
        for i in range(1, page + 1):
            try:
                # url
                url = self.base_url + str(i)
                print url
                # 发送请求
                data = self.send_request(url)
                # print data
                if data == None:
                    break

                # 数据筛选
                proxy_ip_list, count_num = self.analysis_data(data)
                # print proxy_ip_list
                proxy_list += proxy_ip_list
                count += count_num

            except Exception as e:
                print e
        return proxy_list, count


# 正在给代理ip分类:http及https
def distinguish_proxy(proxy_list):
    print '\n正在区分http及https代理类型'
    http_count = 0
    https_count = 0
    http_list = []
    https_list = []
    # 分http及https
    for proxy in proxy_list:
        if proxy.keys() == ['HTTP']:
            http_list.append(proxy)
            http_count += 1
        elif proxy.keys() == ['HTTPS']:
            https_list.append(proxy)
            https_count += 1
    return http_count, https_count, http_list, https_list


# 筛选可用代理ip
def can_use_proxy(proxy_list, count):
    # 筛选可用代理ip
    print '\n正在筛选%s代理ip,\n筛选前个数是：%s' % (proxy_list, count)
    count = 0
    can_use_list = []
    for proxy in proxy_list:
        code = choice_can_use_proxy(proxy)
        # print code
        if code == 200:
            can_use_list.append(proxy)
            count += 1

    return can_use_list, count


# 测试能用的http免费代理
def choice_can_use_proxy(proxy):
    """测试能用的http免费代理"""
    try:
        # 有代理功能的处理器
        proxy_handler = urllib2.ProxyHandler(proxy)
        # openner
        openner = urllib2.build_opener(proxy_handler)
        # 测试是否可用
        response = openner.open('http://www.baidu.com', timeout=3)
        # print response.getcode()
        # print response.read()
        print '%s代理ip测试结果：%s' % (proxy, response.getcode())
        return response.getcode()
    except urllib2.HTTPError, err:
        return err.code
    except urllib2.URLError, err:
        return 666


# 保存可用的代理ip
def proxy_write_file(data, name):
    """保存可用的http代理ip"""
    print '\n正在保存能用的%s代理ip到本地文件' % name
    data = str(data)
    try:
        with open('%s.txt' % name, 'w') as f:
            f.write(data)
    except Exception as e:
        return 'no'
    return "ok"


if __name__ == '__main__':
    print '-------------西刺高匿代理ip下载-------------'
    tool = daili_proxy()

    # 获取代理ip列表
    proxy_list, count = tool.run()
    print '获取到的所有代理ip共:%s个,列表如下:%s' % (count, proxy_list)
    proxy_write_file(proxy_list, 'proxy_list')
    print 'proxy_list代理ip列表保存成功'

    if proxy_list:
        # 区分代理ip类型
        http_count, https_count, http_list, https_list = distinguish_proxy(proxy_list)
        print 'http代理共：%s个,列表如下：%s' % (http_count, http_list)
        print 'https代理：%s个,列表如下：%s' % (https_count, https_list)

        # 筛选可用的代理ip
        http_list, http_count = can_use_proxy(http_list, http_count)
        print 'http代理ip筛选成功%s,\n筛选后个数是：%s' % (http_list, http_count)

        https_list, https_count = can_use_proxy(https_list, https_count)
        print 'https代理ip筛选成功%s,\n筛选后个数是：%s' % (https_list, https_count)

        # 保存
        http_code = proxy_write_file(http_list, 'http_list')
        if http_code == 'no':
            print 'http代理保存到本地失败'
        print 'http代理保存到本地成功'

        https_code = proxy_write_file(https_list, 'https_list')
        if http_code == 'no':
            print 'https代理保存到本地失败'
        print 'https代理保存到本地成功'