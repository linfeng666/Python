# _*_ coding:utf-8 _*_

import json
import csv

# 解决默认编码问题，python2是ascii编码，python3是unicode编码
import sys
reload(sys)
sys.setdefaultencoding('utf-8') # 设置默认编码


def json_to_csv():
    """json格式数据转csv格式"""
    print '请把需要转换的json文件放到该工具同级目录下再使用'
    json_name = raw_input('请输入需要转换的json文件名:')

    # 1/读取json文件
    json_file = open('%s.json' % json_name, 'r')

    # 2/创建csv文件对象
    csv_file = open('%s.csv' % json_name, 'w')

    # 3/创建写入器
    csv_writer = csv.writer(csv_file)
    data_list = json.load(json_file)

    # 4/提取表头
    sheet_title = data_list[0].keys()
    # print sheet_title

    # 5/提取内容
    content_list = []
    for dict_data in data_list:
        content_list.append(dict_data.values())

    # 6/写入表头
    csv_writer.writerow(sheet_title)

    # 7/写入内容
    csv_writer.writerows(content_list)

    # 8/关闭文件
    csv_file.close()
    json_file.close()


if __name__ == '__main__':
    json_to_csv()