# _*_ coding:utf-8 _*_

import urllib2
from lxml import etree

# 筛选可用代理ip
def can_use_proxy():
    # 筛选可用代理ip
    count = 0
    can_use_proxy = []
    with open('proxy_list.txt', 'r') as f:
        data = f.read()
    # print data

    proxy_list = eval(data)
    # print type(proxy_list)
    # print proxy_list

    for proxy in proxy_list:
        code = choice_can_use_proxy(proxy)
        # print code
        if code == 200:
            can_use_proxy.append(proxy)
            count += 1
    return can_use_proxy, count


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

if __name__ == '__main__':
    proxy_list, count = can_use_proxy()
    print '能用的代理ip有：%s个,如下列表\n%s' % (count,proxy_list)